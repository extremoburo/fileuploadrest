# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON

# PIP
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

# DJANGO

# PROJECT
from .imageUpload.serializers import ImageSerializer

# *****************************************************************************
# FUNCTION BASED VIEWS
# http://www.django-rest-framework.org/api-guide/views/#function-based-views
# *****************************************************************************


@api_view(["POST"])  # Probably a PUT method
# Setting the parsers used by this function based view
@parser_classes((FormParser, MultiPartParser))
def upload_image(request):
    """ Upload a new image """

    image_uploaded = request.FILES["image_uploaded"]
    # Should check if the file exists already before saving it.
    destination = open('/home/tanas/' + image_uploaded.name, "wb+")
    for chunk in image_uploaded.chunks():
        destination.write(chunk)
    destination.close()
    return Response({'received request': "File saved"})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_with_model(request):
    """ Upload image and save meta data in database using a model """
    serializer = ImageSerializer(data={
        "name": request.FILES["image_to_upload"].name,
        "image": request.FILES["image_to_upload"]
        }
    )

    if (
        serializer.is_valid(raise_exception=True) and
        request.FILES["image_to_upload"].content_type == "image/png"
    ):
        serializer.save()
        return Response({"response": "serializer is valid"})
