# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON

# PIP
from rest_framework import serializers
from rest_framework import status

# PROJECT
from models import Image


class ImageSerializer(serializers.Serializer):
    image = serializers.FileField(required=True)

    class Meta:
        model = Image
        fields = ("id", "name", "created_at", "size")
