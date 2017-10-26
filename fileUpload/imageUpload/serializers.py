# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON

# PIP
from rest_framework import serializers

# PROJECT
from .models import Image
from .models import ImageForMinio


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ("id", "name", "created_at", "image")


class ImageForMinioSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageForMinio
        fields = ("id", "name", "created_at", "path_to_image", "height", "width", "size")
