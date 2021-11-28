from rest_framework import serializers

from mmb_pf.common_serializers import (
    DateSerializer,
    DateTimeSecSerializer,
    DateTimeSerializer,
    GenderSerializer,
    ImagesSerializer,
    LFPSerializer,
    LFPShortSerializer,
)

from .models import Streets


class StreetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streets
        fields = ["id", "name", "signes"]
        depth = 1
