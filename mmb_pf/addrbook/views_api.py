import json

from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from rest_framework import exceptions, viewsets
from rest_framework.renderers import JSONRenderer

from administration.models import ImageStorage, MMBPFUsers, SystemSettings
from administration.serializers import ImageStorageSerializer
from mmb_pf.common_services import get_constant_models

from .models import CustomSignes, Streets, Teams
from .serializers import CustomSignesSerializer, StreetsSerializer

# from mmb_pf.drf_api import BaseModelPermissions
constant_models = get_constant_models()
iss = ImageStorageSerializer()
###############################################################################
# DRF views
class StreetsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get streets
    """

    renderer_classes = [JSONRenderer]
    queryset = Streets.objects.order_by("name")
    serializer_class = StreetsSerializer

    # permission_classes = [BaseModelPermissions]

    def permission_denied(self, request, message=None, code=None):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")


class CustomSignesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get custom signes
    """

    renderer_classes = [JSONRenderer]
    queryset = CustomSignes.objects.order_by("name")
    serializer_class = CustomSignesSerializer

    # permission_classes = [BaseModelPermissions]

    def permission_denied(self, request, message=None, code=None):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")


###############################################################################
# Custom views
def mmb_map(request):
    """
    get mmb map
    """
    if request.method != "GET":
        return JsonResponse({"msg": "Некорректный метод запроса, только GET"}, status=405)

    mmb_map_image_id = SystemSettings.objects.get_option(name="mmb_map_image_id", default=0)
    map_file = {}
    if mmb_map_image_id:
        try:
            map_file = ImageStorage.objects.get(id=mmb_map_image_id)
        except Exception:
            # will not report any to frontend if id is incorrect
            return JsonResponse(map_file, status=200)
    else:
        return JsonResponse(map_file, status=200)

    return JsonResponse(iss.to_representation(map_file), status=200)


@permission_required("administration.can_change_map", raise_exception=True)
def change_mmb_map(request):
    if request.method != "POST":
        return JsonResponse({"msg": "Некорректный метод запроса, только POST"}, status=405)

    if not request.FILES:
        old_map_id = SystemSettings.objects.get_option(name="mmb_map_image_id", default=0)
        if old_map_id:
            try:
                ImageStorage.objects.get(id=old_map_id).delete()
            except Exception:
                pass

        SystemSettings.objects.set_option(name="mmb_map_image_id", value=0)
        return JsonResponse({"msg": "Карта удалена"}, status=200)

    image_obj = None
    for _, dataobj in request.FILES.items():
        # load only first image if several send
        try:
            image_obj = ImageStorage.objects.create(
                file=dataobj,
                app_name="uploaded_from_api",
                desc="Карта ММБ ПФ",
            )
        except Exception as exc:
            return JsonResponse({"msg": exc.args[0]}, status=422)

        break

    if image_obj:
        old_map_id = SystemSettings.objects.get_option(name="mmb_map_image_id", default=0)
        if old_map_id:
            try:
                ImageStorage.objects.get(id=old_map_id).delete()
            except Exception:
                pass

        SystemSettings.objects.set_option(name="mmb_map_image_id", value=image_obj.id)
        return JsonResponse({"msg": "Карта обновлена"}, status=200)


def addrbook_info(request):
    """
    get addrbook info
    """
    if request.method != "GET":
        return JsonResponse({"msg": "Некорректный метод запроса, только GET"}, status=405)

    addrbook_info_res = {
        "text": SystemSettings.objects.get_option(name="addrbook_text_info", default=""),
        "participants_cnt": MMBPFUsers.objects.filter(
            user_type=constant_models["USER_TYPE"]["names"]["Участник"]
        ).count(),
        "participants_reg_cnt": MMBPFUsers.objects.filter(
            user_type=constant_models["USER_TYPE"]["names"]["Участник"],
            street__isnull=False,
        ).count(),
        "teams_cnt": Teams.objects.all().count(),
    }

    return JsonResponse(addrbook_info_res, status=200)


@permission_required("administration.can_change_info", raise_exception=True)
def change_addrbook_info(request):
    if request.method != "POST":
        return JsonResponse({"msg": "Некорректный метод запроса, только POST"}, status=405)

    new_text_info = None
    try:
        new_text_info = json.loads(request.body)
    except Exception:
        return JsonResponse({"msg": "Тело запроса должно быть json строкой"}, status=415)

    if "text" in new_text_info:
        SystemSettings.objects.set_option(name="addrbook_text_info", value=new_text_info["text"])
        return JsonResponse({"msg": "Информация обновлена"}, status=200)

    return JsonResponse({"msg": "Некорректные данные запроса, не передан ключ text в jsondata"}, status=405)
