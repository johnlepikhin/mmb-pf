from django.http import JsonResponse
from rest_framework import exceptions, mixins, viewsets
from rest_framework.renderers import JSONRenderer

from mmb_pf.common_services import get_constant_models

from .models import CustomSignes, Streets
from .serializers import CustomSignesSerializer, StreetsSerializer

# from mmb_pf.drf_api import BaseModelPermissions


constant_models = get_constant_models()
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

    def permission_denied(self, request, message):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")


class CustomSignesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get custom signes
    """

    renderer_classes = [JSONRenderer]
    queryset = CustomSignes.objects.order_by("name")
    serializer_class = CustomSignesSerializer

    # permission_classes = [BaseModelPermissions]

    def permission_denied(self, request, message):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")


###############################################################################
# Custom views
def mmb_map(request):
    """
    get and change mmb map
    """
    if request.method != "GET":
        return JsonResponse({"msg": "Некорректный метод запроса, только GET"}, status=405, safe=False)

    return JsonResponse({"msg": "mmb map is here"}, status=200, safe=False)
