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
    created_at = models.DateField(auto_now_add=True)
    # No need for size attribute, it is integrated in the image
    # size = models.IntegerField(default=0)

    # Height and Width are also accessible from the "image" attribute
    this_is_the_width = models.PositiveIntegerField()
    this_is_the_height = models.PositiveIntegerField()
    image_format = models.CharField(max_length=1500)
    image = models.ImageField(
        upload_to="subdirectory/to-upload/my-images",
        default="subdirectory/No-img.jpg",
        height_field="this_is_the_height",  # Specifying the attribute to hold height
        width_field="this_is_the_width"  # Same as height
        )

    def __str__(self):
        return "%s" % self.name
