# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON

# PIP
from rest_framework import serializers

# PROJECT
from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ("id", "name", "created_at", "image")
