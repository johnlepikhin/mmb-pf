import re
from datetime import datetime, timedelta
from urllib.parse import unquote

from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import exception_handler

from mmb_pf.common_services import get_timezone


def custom_exception_handler(exc, context):
    """
    This handler is used by drf when something going wrong
    """
    response = exception_handler(exc, context)
    # just want 1 string
    msg_final = ""
    exc_msg = ""
    # get additinal info if exists
    if getattr(exc, "detail", None):
        if "msg" in exc.detail:
            exc_msg = exc.detail["msg"]
        elif isinstance(exc.detail, list):
            exc_msg = "; ".join(exc.detail)
        else:
            exc_msg = exc.detail
    elif getattr(exc, "args", None):
        exc_msg = exc.args[0]
    else:
        exc_msg = str(exc)

    if isinstance(exc_msg, dict):
        for key, val in exc_msg.items():
            if isinstance(val, list):
                msg_final += f'{key}: {"; ".join(val)};'
            else:
                msg_final += f"{key}: {val};"
    else:
        msg_final += str(exc_msg)
    # add class name
    msg_final += f" [{type(exc).__name__}]"

    if response and response.status_code == 403:
        return JsonResponse({"msg": f"{msg_final}"}, safe=False, status=403)
    elif response and response.status_code == 404:
        return JsonResponse({"msg": f'{"Данные не найдены"}'}, safe=False, status=404)
    else:
        return JsonResponse({"msg": f"{msg_final}"}, safe=False, status=422)

    return response


def request_fields_parser(**kwargs):
    """
    This parser used in drf for checking url parameters
    TAKE:
        request=request object,
        fields={}, # fields names: types
        reqtype='drf', # by default drf / from_request / predefined
        predefined={}, # fields data for predefined reqtype, will be used instead of request object
    RETURN:
        {} - ready for query params

    Field types:
        bool - should be boolean type
        int - should be int or convertable to int
        positive_int - should be positive int or convertable to int
        str - should be string or convertable to string
        list - should be list for __in requests
        str_capitalize - should be string or convertable to string and result will be capitalized
        str_contains - should be string or convertable to string and result will be filtered as regexp with case case-sensitive
        str_contains_last10 - should be string or convertable to string and result will be filtered as regexp with case case-sensitive, last 10 symbols
        custom_date - date in the this system custom format DD.MM.YYYY
        lte_custom_date/gte_custom_date - date in the this system custom format DD.MM.YYYY + less then or greater then
        custom_datetime - date in the this system custom format DD.MM.YYYY HH:MM
        custom_datetime_autodetect - date or datetime will be expected DD.MM.YYYY or DD.MM.YYYY HH:MM
        lte_plus_days - this param for date, should be int or convertable to int, current date will be + defined days and returned as less or equal
    """

    query_params = {}
    timezone = get_timezone()
    if "fields" not in kwargs:
        raise exceptions.ParseError(f"Не передан параметр fields")
    if "reqtype" not in kwargs:
        kwargs["reqtype"] = "drf"

    if (kwargs["reqtype"] == "drf" or kwargs["reqtype"] == "from_request") and "request" not in kwargs:
        raise exceptions.ParseError(f"Не передан параметр request")
    if kwargs["reqtype"] == "predefined" and "predefined" not in kwargs:
        raise exceptions.ParseError(f"Не передан параметр predefined")

    for field in kwargs["fields"]:
        field_data = None
        if kwargs["reqtype"] == "drf":
            field_data = kwargs["request"].query_params.get(field, None)
        elif kwargs["reqtype"] == "predefined":
            field_data = kwargs["predefined"][field]
        elif kwargs["reqtype"] == "from_request":
            if field in kwargs["request"].GET:
                field_data = kwargs["request"].GET[field]
            else:
                field_data = None
                # raise exceptions.ParseError(f'Не передан обязательный параметр: "{field}"')

        if field_data:
            # This fields types are not change field key and can be used with predefined mode
            if kwargs["fields"][field] == "bool":
                if field_data in ["true", "false"]:
                    field_data = True if field_data == "true" else False
                else:
                    raise exceptions.ParseError(f'Поле "{field}" может иметь только true/false значения')
            elif kwargs["fields"][field] == "int":
                try:
                    field_data = int(field_data)
                except:
                    raise exceptions.ParseError(f'Поле "{field}" может иметь только числовые значения') from None
            elif kwargs["fields"][field] == "positive_int":
                try:
                    field_data = int(field_data)
                except:
                    raise exceptions.ParseError(
                        f'Поле "{field}" может иметь только положительные числовые значения'
                    ) from None
                if field_data < 1:
                    raise exceptions.ParseError(f'Поле "{field}" может иметь только положительные числовые значения')
            elif kwargs["fields"][field] == "str":
                try:
                    field_data = unquote(field_data)
                except:
                    raise exceptions.ParseError(f'Поле "{field}" может иметь только строковые значения') from None
            elif kwargs["fields"][field] == "str_capitalize":
                try:
                    field_data = unquote(field_data).capitalize()
                except:
                    raise exceptions.ParseError(f'Поле "{field}" может иметь только строковые значения') from None
            elif kwargs["fields"][field] == "custom_date":
                try:
                    field_data = datetime.strptime(field_data, "%d.%m.%Y").astimezone(timezone)
                except:
                    raise exceptions.ParseError(f'Поле "{field}" должно иметь формат "ДД.ММ.ГГГГ"') from None
            elif kwargs["fields"][field] == "custom_datetime":
                try:
                    field_data = datetime.strptime(field_data, "%d.%m.%Y %H:%M").astimezone(timezone)
                except:
                    raise exceptions.ParseError(f'Поле "{field}" должно иметь формат "ДД.ММ.ГГГГ ЧЧ:MM"') from None
            # This field types are change field key and can not be used with predefined mode (in this mode key changed already)
            if kwargs["reqtype"] != "predefined":
                if kwargs["fields"][field] == "list":
                    try:
                        field_data = list(field_data.split(","))
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" должно быть списком 1,2,3') from None
                    field = field + "__in"
                elif kwargs["fields"][field] == "str_contains":
                    try:
                        field_data = unquote(field_data)
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" может иметь только строковые значения') from None
                    field = field + "__icontains"
                elif kwargs["fields"][field] == "str_contains_last10":
                    try:
                        field_data = unquote(field_data)
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" может иметь только строковые значения') from None
                    field = field + "__icontains"

                    # Will compare only 10 last symbols for +7 and 8 numbers detection
                    if len(field_data) > 9:
                        field_data = field_data[-10:]
                    else:
                        if re.match(r"^\+\d+$", field_data):
                            field_data = re.match(r"^\+(\d+)$", field_data).group(1)
                elif kwargs["fields"][field] == "lte_custom_date":
                    try:
                        field_data = datetime.strptime(field_data, "%d.%m.%Y").astimezone(timezone)
                        field = field + "__lte"
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" должно иметь формат "ДД.ММ.ГГГГ"') from None
                elif kwargs["fields"][field] == "gte_custom_date":
                    try:
                        field_data = datetime.strptime(field_data, "%d.%m.%Y").astimezone(timezone)
                        field = field + "__gte"
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" должно иметь формат "ДД.ММ.ГГГГ"') from None
                elif kwargs["fields"][field] == "custom_datetime_autodetect":
                    try:
                        field_data = datetime.strptime(field_data, "%d.%m.%Y %H:%M").astimezone(timezone)
                    except:
                        try:
                            field = field + "__date"
                            field_data = datetime.strptime(field_data, "%d.%m.%Y").astimezone(timezone)
                        except:
                            raise exceptions.ParseError(
                                f'Поле "{field}" должно иметь формат "ДД.ММ.ГГГГ" или "ДД.ММ.ГГГГ ЧЧ:MM"'
                            ) from None
                elif kwargs["fields"][field] == "lte_plus_days":
                    try:
                        field_data = datetime.now().astimezone(timezone) + timedelta(days=int(field_data))
                        field = field + "__lte"
                    except:
                        raise exceptions.ParseError(f'Поле "{field}" должно содержать целое количество дней') from None

            query_params[field] = field_data

    return query_params


class BaseModelPermissions(DjangoModelPermissions):
    """
    This class is used by drf for checking permissions, from standard django model permissions
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_object_permission(self, request, view, obj):
        has_permission = super().has_permission(request, view)

        if has_permission and view.action == "retrieve":
            return self._queryset(view).filter(pk=obj.pk).exists()

        if has_permission and view.action == "update":
            return self._queryset(view).filter(pk=obj.pk).exists()

        if has_permission and view.action == "partial_update":
            return self._queryset(view).filter(pk=obj.pk).exists()

        if has_permission and view.action == "destroy":
            return self._queryset(view).filter(pk=obj.pk).exists()

        return False
