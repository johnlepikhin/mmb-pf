from datetime import datetime, timedelta

from rest_framework import serializers

from mmb_pf.common_services import get_constant_models, get_timezone

timezone = get_timezone()
constant_models = get_constant_models()


class LFPShortSerializer(serializers.SerializerMethodField):
    def to_internal_value(self, data):
        """Not used"""
        return

    def to_representation(self, value):
        name = ""
        if value:
            if hasattr(value, "last_name") and value.last_name:
                name = value.last_name.capitalize()
            if hasattr(value, "first_name") and value.first_name:
                name += f" {value.first_name[0].capitalize()}."
            if hasattr(value, "patronymic") and value.patronymic:
                name += f"{value.patronymic[0].capitalize()}."
            return name

        return None


class LFPSerializer(serializers.SerializerMethodField):
    def to_internal_value(self, data):
        """Not used"""
        return

    def to_representation(self, value):
        if value:
            return f"{value.last_name} {value.first_name} {value.patronymic}".rstrip()
        else:
            return None


class PersonalNamesSerializer(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if data:
            return data.capitalize()
        else:
            return None


class GenderSerializer(serializers.Field):
    def to_representation(self, value):
        if value:
            return constant_models["GENDER"]["keys"][value]
        else:
            return None

    def to_internal_value(self, data):
        if data:
            return constant_models["GENDER"]["names"][data]
        else:
            return None


class DateSerializer(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.strftime("%d.%m.%Y")
        else:
            return None

    def to_internal_value(self, data):
        if data:
            return datetime.strptime(data, "%d.%m.%Y")
        else:
            return None


class DateTimeSerializer(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.astimezone(timezone).strftime("%d.%m.%Y %H:%M")
        else:
            return None

    def to_internal_value(self, data):
        if data:
            return datetime.strptime(data, "%d.%m.%Y %H:%M").astimezone(timezone)
        else:
            return None


class DateTimeSecSerializer(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.astimezone(timezone).strftime("%d.%m.%Y %H:%M:%S")
        else:
            return None

    def to_internal_value(self, data):
        if data:
            return datetime.strptime(data, "%d.%m.%Y %H:%M:%S").astimezone(timezone)
        else:
            return None


class DateTimeJSONSerializer(serializers.Field):
    """Convert to/from json date"""

    def to_representation(self, value):
        if value:
            return value.astimezone(get_timezone("utc")).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        else:
            return None

    def to_internal_value(self, data):
        if data:
            # TODO: Cant found how convert json utc time to local
            return datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=3)
        else:
            return None


class ImagesSerializer(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        """Not used"""
        return

    def to_representation(self, value):
        if value:
            converted = []
            for image_obj in value.iterator():
                converted.append(
                    {
                        "id": image_obj.id,
                        "href": image_obj.file.url,
                        "desc": image_obj.desc,
                    }
                )
            return converted
        else:
            return None
