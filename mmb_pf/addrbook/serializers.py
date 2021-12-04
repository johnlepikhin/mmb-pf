from rest_framework import serializers

from .models import CustomSignes, Streets, StreetSignes


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
