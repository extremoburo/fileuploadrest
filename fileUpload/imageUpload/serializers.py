# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON

# PIP
from rest_framework import serializers
from rest_framework import status

# PROJECT
from .models import Image


class ImageSerializer(serializers.Serializer):
    image = serializers.FileField(required=False)

    class Meta:
        model = Image
        fields = ("id", "name", "created_at", "size", "image")

    def validate(self, data):
        return data

    def create(self, validated_data):
        return Image.objects.create(**validated_data)
