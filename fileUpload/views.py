# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON
import traceback

# PIP
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from minio import Minio
from minio.error import ResponseError
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists

# DJANGO
from django.conf import settings

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
        (
            request.FILES["image_to_upload"].content_type == "image/png" or
            request.FILES["image_to_upload"].content_type == "image/jpeg"
        )
    ):
        serializer.save()
        return Response({"response": "serializer is valid"})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_to_minio(request):
    """ Upload image, save meta data and save to minio """
    myRequest = request
    image = myRequest.FILES["image_to_upload"]
    # How to prevent the save locally?
    # Save directly to minio, and keep info to fetch it from minio
    minioClient = Minio(
        'localhost:9000',
        access_key="A2P6XIHNB1BFHCAOJOK9",  # Depends on the user
        secret_key="44JvW89En4gwd6UpnAPYISjIW9JoNctNAcaxHPs+",  # Depends on the user
        secure=False  # Not over SSL. Should probably be changed
    )
    # Maybe saving to minio should be after serializer.save()
    serializer = ImageSerializer(data={
        "name": image.name,
        "image": image
        }
    )

    if (
        serializer.is_valid(raise_exception=True) and
        (
            image.content_type == "image/jpeg" or
            image.content_type == "image/png"
        )
    ):
        serializer.save()
        # Copying file from disk into a minio bucket
        if(minioClient.bucket_exists("anas")):
            try:
                path_of_image = settings.BASE_DIR + serializer.data["image"]
                minioClient.fput_object("anas", image.name, path_of_image)
            except ResponseError as err:
                print(err)

        return Response({"response": "serializer is valid"})


"""
    try:
        minioClient.make_bucket("useruploads2", location="us-east-1")
    except BucketAlreadyOwnedByYou as err:
        # If the bucket is owned by the client
        try:
            minioClient.fput_object("useruploads2", image.name, "/home/tanas/Storepilots/FileUpload/media/subdirectory/to-upload/my-images/pexels-photo-620332.jpeg")
        except ResponseError as err:
            print(err)
    #except BucketAlreadyExists as err:
    #    pass
    except ResponseError as err:
        raise
    else:
        try:
            # https://docs.minio.io/docs/python-client-api-reference#fput_object
            minioClient.fput_object("useruploads2", image.name, "/home/tanas/Storepilots/FileUpload/media/subdirectory/to-upload/my-images/pexels-photo-620332.jpeg")
        except ResponseError as err:
            print(err)

"""
