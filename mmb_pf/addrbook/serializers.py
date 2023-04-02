import datetime

from rest_framework import exceptions, serializers

from mmb_pf.common_serializers import DateTimeSecSerializer
from mmb_pf.common_services import get_timezone

from .models import CustomSignes, Streets, StreetSignes, Teams

timezone = get_timezone()


class StreetsSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data and "id" in data:
            return Streets.objects.get(id=data["id"])

        return None

    class Meta:
        model = Streets
        fields = ("id", "name", "signes")
        depth = 1


class StreetSignesSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data and "id" in data:
            return StreetSignes.objects.get(id=data["id"])

        return None

    class Meta:
        model = StreetSignes
        fields = (
            "id",
            "name",
        )


class CustomSignesSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data and "id" in data:
            return CustomSignes.objects.get(id=data["id"])

        return None

    class Meta:
        model = CustomSignes
        fields = (
            "id",
            "name",
        )


class TeamsSerializer(serializers.ModelSerializer):
    finished_date = DateTimeSecSerializer()

    def update(self, instance, validated_data):
        # Before object.save
        # instance - OLD data
        # validated_data - NEW data
        if instance.finished:
            raise exceptions.ValidationError(
                f"Команда {instance.team_id} уже финишировала, сбросьте finished через"
                + " админку для повторного выставления значения через api"
            )

        if validated_data.get("finished", False):
            if "finished_date" not in validated_data:
                validated_data["finished_date"] = datetime.datetime.now().astimezone(timezone)
        else:
            if "finished" not in validated_data:
                validated_data["finished"] = True

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = Teams
        read_only_fields = ("id", "team_id", "name")
        fields = "__all__"
