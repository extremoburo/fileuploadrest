# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON


# PIP

# DJANGO
from django.db import models

# PROJECT


class Image(models.Model):
    # name = models.CharField(max_length=1000, required=True)
    name = models.CharField(max_length=1000)
    # created_at = models.DateField(auto_add_now=True)
    created_at = models.DateField(auto_now_add=True)
    size = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    image_format = models.CharField(max_length=1500)
    image = models.ImageField(upload_to="subdirectory/to-upload/my-images", default="subdirectory/No-img.jpg")

    def __str__(self):
        return "%s" % self.name
