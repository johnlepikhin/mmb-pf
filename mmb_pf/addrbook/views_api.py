from rest_framework import exceptions, mixins, viewsets
from rest_framework.renderers import JSONRenderer

from mmb_pf.common_services import get_constant_models
from mmb_pf.drf_api import BaseModelPermissions

from .models import Streets
from .serializers import StreetsSerializer

constant_models = get_constant_models()
###############################################################################
# DRF views
class StreetsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get streets
    """

    renderer_classes = [JSONRenderer]
    queryset = Streets.objects.filter().values().order_by("name")
    serializer_class = StreetsSerializer
    # permission_classes = [BaseModelPermissions]

    def permission_denied(self, request, message):
        raise exceptions.PermissionDenied("У вас нет прав для выполнения данного запроса")
