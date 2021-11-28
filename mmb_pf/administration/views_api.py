import json
import re

from django.contrib.auth import password_validation, update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework import exceptions, mixins, viewsets
from rest_framework.renderers import JSONRenderer

from mmb_pf.common_services import get_constant_models
from mmb_pf.drf_api import BaseModelPermissions, request_fields_parser

from .models import MMBPFUsers
from .serializers import MMBPFUserListSerializer, MMBPFUserSerializer

constant_models = get_constant_models()
###############################################################################
# DRF views
class MMBPFUsersViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API Endpoint for users, without create/delete actions
    """

    renderer_classes = [JSONRenderer]
    # queryset = QuerySet(model=MMBPFUsers, query=user_type=constant_models["USER_TYPE"]["names"]["Участник"]).order_by("team"))
    queryset = MMBPFUsers.objects.filter(user_type=constant_models["USER_TYPE"]["names"]["Участник"]).order_by("team")
    serializer_class = MMBPFUserSerializer  # used when PATCH (modify operations)

    action_serializers = {
        "retrieve": MMBPFUserSerializer,  # Get one elem
        "list": MMBPFUserListSerializer,  # get all elems
    }
    # it opened for everyone
    # permission_classes = [BaseModelPermissions]

    def get_queryset(self):
        queried_fields = {
            "id": "int",
            "is_active": "bool",
            "first_name": "str_capitalize",
            "last_name": "str_capitalize",
            "patronymic": "str_capitalize",
            "birth": "custom_date",
            "phone": "str_contains_last10",
            "tourist_club": "str",
        }
        query_params = request_fields_parser(request=self.request, fields=queried_fields)

        if self.action == "list":
            if query_params:
                queryset = self.queryset.filter(**query_params)
            else:
                queryset = self.queryset

            # TODO: probably add backend query compose to the frontend
            # if queryset.count() > 1000 and not query_params:
            #     queryset = queryset.all()[:1000]
        else:
            queryset = self.queryset

        # this slice needed for droppting django queryset cache
        return queryset[: queryset.count()]

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super(MMBPFUsersViewSet, self).get_serializer_class()

    def permission_denied(self, request, message, code):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")


###############################################################################
# Custom views
@permission_required("administration.change_my_password", raise_exception=True)
def change_my_password(request):
    """
    Current user password changer

    """
    if request.method != "POST":
        return JsonResponse({"msg": "Некорректный метод запроса, только POST"}, status=405, safe=False)

    try:
        request_body = json.loads(request.body)
    except Exception:
        return JsonResponse({"msg": "Некорректное тело запроса, только JSON"}, status=422, safe=False)
    if not request_body:
        return JsonResponse({"msg": "Запрос без параметров для изменения"}, status=422, safe=False)

    # check fields
    fields = {
        "old_password": "re:^.{4,}$",
        "new_password": "re:^.{4,}$",
    }
    for field in request_body:
        if not field in fields:
            return JsonResponse({"msg": f'Поле "{field}" некорректное для данного запроса'}, status=422, safe=False)
        check_type = fields[field]
        if re.match(r"^re:.+", check_type):
            regexp = re.match(r"^re:(.+)$", check_type).group(1)
            if not re.match(regexp, str(request_body[field])):
                return JsonResponse(
                    {"msg": f'Поле "{field}" имеет неверный формат или значение'}, status=422, safe=False
                )

    try:
        user_obj = MMBPFUsers.objects.get(id=request.user.id)
    except Exception:
        return JsonResponse({"msg": "Ошибка запроса базы данных"}, status=422, safe=False)

    # check
    if user_obj.check_password(request_body["old_password"]):
        try:
            password_validation.validate_password(password=request_body["new_password"], user=user_obj)
        except Exception as exc:
            err_str = " ".join(exc)
            return JsonResponse({"msg": f"{err_str}"}, status=422, safe=False)

        user_obj.set_password(request_body["new_password"])
        user_obj.save()
        update_session_auth_hash(request, user_obj)
    else:
        return JsonResponse({"msg": "Введён некорректный текущий пароль"}, status=422, safe=False)

    return JsonResponse({"msg": "Изменения сохранены"}, status=200, safe=False)
