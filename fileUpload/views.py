# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON

# PIP
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
# from requests import post

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
    # pythonDict = dict(queryDictReceived)
    return Response({'received request': "File saved"})
# queryDictReceived = request._request  #.GET


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_with_model(request):
    """ Upload image and save meta data in database using a model """
    # queryset =
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        # serializer.image = request.FILES["image_uploaded"]
        # serializer.image = "test"
        serializer.name = request.FILES["image_uploaded"].name
        serializer.save()
        return Response({"response": "serializer is valid"})
    else:
        return Response({"response": "serializer is INvalid"})

    def perform_create(self, serializer):
        # file_obj = self.validated_data["image_uploaded"]
        # file_obj.save()
        serializer.save(image=self.request.FILES["image_uploaded"])
