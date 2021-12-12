import json
from collections import OrderedDict

from rest_framework import exceptions, serializers

from addrbook.serializers import (
    CustomSignesSerializer,
    StreetSignesSerializer,
    StreetsSerializer,
)
from administration.models import ImageStorage, ParticipantCardActionsJournal
from mmb_pf.common_serializers import (
    DateSerializer,
    DateTimeSecSerializer,
    DateTimeSerializer,
    GenderSerializer,
    LFPSerializer,
    LFPShortSerializer,
)
from mmb_pf.common_services import get_timezone

from .models import (
    ImageStorage,
    MMBPFUsers,
    ParticipantCardActionsJournal,
    SystemSettings,
)

timezone = get_timezone()
lfps = LFPSerializer()
max_images_per_user = SystemSettings.objects.get_option(name="max_images_per_user", default=5)


class ImageStorageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    href = serializers.CharField(source="file.url")

    class Meta:
        model = ImageStorage
        exclude = ["app_name", "file"]


class MMBPFUserSerializer(serializers.ModelSerializer):
    modification_date = DateTimeSecSerializer()
    images = ImageStorageSerializer(required=False, allow_null=True, many=True)
    date_joined = DateTimeSerializer(read_only=True)
    gender = GenderSerializer()
    birth = DateSerializer(allow_null=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    street = StreetsSerializer(required=True, allow_null=False)
    sign = StreetSignesSerializer(required=True, allow_null=False)
    custom_sign = CustomSignesSerializer(required=False, allow_null=True)

    class Meta:
        model = MMBPFUsers
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "user_permissions",
            "groups",
            "user_type",
            "team",
            # they are not work in the forest
            "email",
            "phone",
        ]
        read_only_fields = (
            "is_active",
            "modification_date",
            "date_joined",
            "last_login",
            "username",
            "gender",
            "first_name",
            "last_name",
            "birth",
            "patronymic",
            "tourist_club",
        )
        depth = 1

    def to_internal_value(self, data):
        # data sends by form type, so we have to catch all things right
        internal_value = super(MMBPFUserSerializer, self).to_internal_value(json.loads(data.get("jsondata")))
        if (max_images_per_user + 1) < (len(data) + len(internal_value["images"])):
            raise exceptions.ValidationError(
                {"Максимально допустимое количество изображений для участника:": max_images_per_user}
            )

        for datakey, dataobj in data.items():
            if datakey == "jsondata":
                continue

            img_obj = ImageStorage.objects.create(
                file=dataobj,
                app_name="uploaded_from_api",
                desc="",
            )
            internal_value["images"].append(
                OrderedDict(
                    [
                        ("id", img_obj.id),
                        ("file", {"url": img_obj.file.url}),
                        ("desc", img_obj.desc),
                    ]
                )
            )

        return internal_value

    def update(self, instance, validated_data):
        # Before object.save
        # instance - OLD data
        # validated_data - NEW data

        # check modification_date
        if validated_data.get("modification_date", None):
            if validated_data["modification_date"].astimezone(
                get_timezone("utc")
            ) != instance.modification_date.replace(microsecond=0):
                raise exceptions.ValidationError(
                    "Другой пользователь изменил данные этой карточки, к сожалению ваши данные не могут быть сохранены "
                    + "обновите форму и введите их заново"
                )
        else:
            raise exceptions.ValidationError("Поле 'modification_date' является обязательным")

        changed_data = []
        for attr, value in validated_data.items():
            if attr != "modification_date" and value != getattr(instance, attr):
                changed_data.append(f"Изменение {attr}: {value}")

            if attr == "images":
                will_removed_ids = []
                stay_images_ids = [obj["id"] for obj in validated_data["images"]]
                for old_img_id in instance.images.all().values_list("id", flat=True):
                    if old_img_id not in stay_images_ids:
                        will_removed_ids.append(old_img_id)

                instance.images.set(stay_images_ids)
                if SystemSettings.objects.get_option(name="delete_user_img_from_disk", default=True):
                    for img_id in will_removed_ids:
                        ImageStorage.objects.get(id=img_id).delete()

            else:
                setattr(instance, attr, value)

        instance.save()

        # store in journal
        if not changed_data:
            changed_data.append("Изменение данных карточки")

        ParticipantCardActionsJournal.objects.add_to_journal(
            serializer=self,
            participant_id=instance.id,
            desc="; ".join(changed_data),
        )

        return instance


class MMBPFUserListSerializer(serializers.ModelSerializer):
    lfp = LFPSerializer()
    lfps = LFPShortSerializer()

    street_name = serializers.CharField(source="street.name", read_only=True, allow_null=True)
    sign_name = serializers.CharField(source="sign.name", read_only=True, allow_null=True)
    custom_sign_name = serializers.CharField(source="custom_sign.name", read_only=True, allow_null=True)

    class Meta:
        model = MMBPFUsers
        fields = [
            "id",
            "lfp",
            "lfps",
            "is_active",
            "username",
            "tourist_club",
            "team",
            "street_name",
            "sign_name",
            "custom_sign_name",
            "user_desc",
        ]
        depth = 1


class ParticipantCardActionsJournalSerializer(serializers.ModelSerializer):
    creation_date = DateTimeSerializer()

    class Meta:
        model = ParticipantCardActionsJournal
        exclude = ["id"]
