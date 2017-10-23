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
# from serializers import ImageSerializer

# *****************************************************************************
# FUNCTION BASED VIEWS
# http://www.django-rest-framework.org/api-guide/views/#function-based-views
# *****************************************************************************


@api_view(["POST"])  # Probably a PUT method
# Setting the parsers used by this function based view
@parser_classes((FormParser, MultiPartParser))
def upload_image(request):
    """ Upload a new image """

    # serializer = ImageSerializer(data=request.data)
    image_uploaded = request.FILES["image_uploaded"]
    destination = open('/home/tanas/' + image_uploaded.name, "wb+")
    for chunk in image_uploaded.chunks():
        destination.write(chunk)
    destination.close()
    # pythonDict = dict(queryDictReceived)
    return Response({'received request': "File saved"})



# queryDictReceived = request._request  #.GET   # 
    