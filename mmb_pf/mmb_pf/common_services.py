import json
import re
from functools import wraps
from typing import Callable, Dict

import pytz  # typing: ignore
from django.http import JsonResponse
from pytz import timezone
from rest_framework import exceptions

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


def check_api_request(checks: Dict) -> Callable:
    """
    Universal decorator for api requests checks
    use request django object
    Args:
        checks: {
            methods: ['GET', 'POST'], # methods accepted
            json_keys: {
                event_id: "[0-9]{3}",
                old_password: ".{4,}"
            }
            get_keys: {
                schedule_id: "[0-9]{3}",
            }
            optional_keys: False, # define true if only if key defined - it should be checked
        }
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                request = args[0]
            else:
                request = kwargs.get("request")

            if not request or not hasattr(request, "method"):
                raise exceptions.APIException("request parameter not passed or incorrect for api checker")

            if "methods" in checks:
                if request.method not in checks["methods"]:
                    return JsonResponse(
                        {"msg": f"Некорректный метод запроса, принимаются только {checks['methods']}"}, status=405
                    )
            if "json_keys" in checks:
                try:
                    request_body = json.loads(request.body)
                except Exception:
                    return JsonResponse({"msg": "Некорректное тело запроса, только JSON"}, status=422)

                for field, regexp in checks["json_keys"].items():
                    if not request_body.get(field):
                        if not checks.get("optional_keys", False):
                            return JsonResponse({"msg": f'Поле "{field}" не передано'}, status=422)
                        continue
                    if not re.fullmatch(regexp, str(request_body[field])):
                        return JsonResponse({"msg": f'Поле "{field}" имеет неверный формат или значение'}, status=422)
            if "get_keys" in checks:
                for field, regexp in checks["get_keys"].items():
                    if not request.GET.get(field):
                        if not checks.get("optional_keys", False):
                            return JsonResponse({"msg": f'Поле "{field}" не передано'}, status=422)
                        continue
                    if not re.fullmatch(regexp, str(request.GET[field])):
                        return JsonResponse({"msg": f'Поле "{field}" имеет неверный формат или значение'}, status=422)

            return func(*args, **kwargs)

        return wrapper

    return decorator
