from rest_framework import exceptions, serializers

from addrbook.serializers import (
    CustomSignesSerializer,
    StreetSignesSerializer,
    StreetsSerializer,
)
from administration.models import ParticipantCardActionsJournal
from mmb_pf.common_serializers import (
    DateSerializer,
    DateTimeSecSerializer,
    DateTimeSerializer,
    GenderSerializer,
    ImagesSerializer,
    LFPSerializer,
    LFPShortSerializer,
)
from mmb_pf.common_services import get_timezone

from .models import MMBPFUsers, ParticipantCardActionsJournal

timezone = get_timezone()
lfps = LFPSerializer()


class MMBPFUserSerializer(serializers.ModelSerializer):
    modification_date = DateTimeSecSerializer()
    images = ImagesSerializer(read_only=True)
    date_joined = DateTimeSerializer(read_only=True)
    gender = GenderSerializer()
    birth = DateSerializer(allow_null=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    street = StreetsSerializer(required=True, allow_null=False)
    sign = StreetSignesSerializer(required=True, allow_null=False)
    custom_sign = CustomSignesSerializer(required=False, allow_null=True)
    # user_ranks = serializers.PrimaryKeyRelatedField(many=True, queryset=ESSUserRanks.objects.all())

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

    # def to_internal_value(self, data):
    #     # catch password from request and store it to internal value
    #     # because i dont send it, and drf decline unknown field by default
    #     internal_value = super(ESSUserSerializer, self).to_internal_value(data)
    #     password = data.get("password")
    #     if password:
    #         internal_value.update({"password": password})
    #     return internal_value

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
            raise exceptions.ValidationError(f"Поле 'modification_date' является обязательным")

        changed_data = []

        # if instance.is_active and not validated_data["is_active"]:
        #     changed_data.append("Блокировка аккаунта")
        # elif not instance.is_active and validated_data["is_active"]:
        #     changed_data.append("Разблокировка аккаунта")

        # if [ur for ur in instance.user_ranks.all()] != validated_data["user_ranks"]:
        #     user_rank_changed = True
        #     changed_data.append(f"Изменение рангов: {'; '.join(obj.name for obj in validated_data['user_ranks'])}")

        skipped_fileds = [
            "images",
        ]
        for attr, value in validated_data.items():
            if attr in skipped_fileds:
                continue

            if attr != "modification_date" and value != getattr(instance, attr):
                changed_data.append(f"Изменение {attr}: {value}")

            if attr == "user_ranks":
                instance.user_ranks.set(validated_data["user_ranks"])
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
