# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON

# PIP

# DJANGO
from django.db import models

# PROJECT


class Image(models.Model):
    name = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    image_format = models.CharField(max_length=1500)
    image = models.ImageField(
        upload_to="subdirectory/to-upload/my-images",
        default="subdirectory/No-img.jpg",
        height_field="height",  # Specifying the attribute to hold height
        width_field="width"  # Same as height_field
        )

    def __str__(self):
        return "%s" % self.name
