import pytz  # typing: ignore
from pytz import timezone

from mmb_pf import settings


def get_timezone(zone_type=None):
    """used for get timezone from one place"""
    if not zone_type:
        zone = timezone(settings.TIME_ZONE)
    elif zone_type == "utc":
        zone = pytz.utc
    return zone


def get_constant_models():
    # genders
    MALE = 1
    FEMALE = 2

    # user types
    ADMINISTRATION = 1  # this is INTERNAL people, they could use whole system
    USERS = 2  # this is EXTERNAL people, they can get access to personnel private cabinet only

    constants = {
        "GENDER": {
            "keys": {  # used in the serializers for representation
                MALE: "Мужской",
                FEMALE: "Женский",
            },
            "names": {  # used in serializers and model requests
                "Мужской": MALE,
                "Женский": FEMALE,
            },
            "choices": (
                (MALE, "Мужской"),
                (FEMALE, "Женский"),
            ),
            "default": MALE,
        },
    }

    return constants
