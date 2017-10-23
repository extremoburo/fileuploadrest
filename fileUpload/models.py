# *****************************************************************************
# IMPORTS
# *****************************************************************************


# PYTHON


# PIP

# DJANGO
from django.db import models

# PROJECT


class Image(models.Model):
    name = models.CharField(max_length=1000, reuired=True)
    created_at = models.DateField(auto_add_now=True)
    size = models.IntegerField(default=0)
