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
    male_id = 1
    female_id = 2

    # user types
    administration_id = 1  # user accounts for administration_id
    participant_id = 2  # user accounts of participant_ids - they are could be removed

    constants = {
        "GENDER": {
            "keys": {  # used in the serializers for representation
                male_id: "Мужской",
                female_id: "Женский",
            },
            "names": {  # used in serializers and model requests
                "Мужской": male_id,
                "Женский": female_id,
            },
            "choices": (
                (male_id, "Мужской"),
                (female_id, "Женский"),
            ),
            "default": male_id,
        },
        "USER_TYPE": {
            "names": {
                "Организатор": administration_id,
                "Участник": participant_id,
            },
            "choices": (
                (administration_id, "Организатор"),
                (participant_id, "Участник"),
            ),
            # ! IMPORTANT ! With this value new users created and removed by cleanup
            "default": participant_id,
        },
    }

    return constants
