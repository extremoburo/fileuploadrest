# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON

# PIP
from PIL import Image
from minio import Minio
from minio.error import ResponseError
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
# from minio.error import BucketAlreadyOwnedByYou
# from minio.error import BucketAlreadyExists

# DJANGO
from django.conf import settings

# PROJECT
from .imageUpload.serializers import ImageForMinioSerializer
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
    # Should check if the file exists already before saving it
    destination = open('/home/tanas/' + image_uploaded.name, "wb+")
    for chunk in image_uploaded.chunks():
        destination.write(chunk)
    destination.close()
    return Response({'received request': "File saved"})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_with_model(request):
    """Upload image and save meta data in database using a model"""
    serializer = ImageSerializer(data={
        "name": request.FILES["image_to_upload"].name,
        "image": request.FILES["image_to_upload"]
        }
    )
    if serializer.is_valid(raise_exception=True) and is_image(image.content_type):
        serializer.save()
        return Response({"response": "serializer is valid"})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_to_minio(request):
    """ Upload image, save it to disk THEN and save it to Minio """
    myRequest = request
    image = myRequest.FILES["image_to_upload"]
    # How to prevent the save locally?
    # Save directly to minio, and keep info to fetch it from minio
    minioClient = Minio(
        'localhost:9000',
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False  # Not over SSL. Should probably be changed
    )
    serializer = ImageSerializer(data={
        "name": image.name,
        "image": image
        }
    )

    if serializer.is_valid(raise_exception=True) and is_image(image.content_type):
        serializer.save()
        # Copying file from disk into a minio bucket
        if(minioClient.bucket_exists("anas")):
            try:
                # serializer.data["image"] is the relative path to the image
                path_of_image = settings.BASE_DIR + serializer.data["image"]
                minioClient.fput_object("anas", image.name, path_of_image)
            except ResponseError as err:
                print(err)

        return Response({"response": "serializer is valid"})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_to_minio_directly(request):
    """
    Upload image, and save it to Minio directly.
    Unlike the previous view, this should not leave behind a file in the disk.
    """
    myRequest = request
    image = myRequest.FILES["image_to_upload"]
    minioClient = Minio(
        'localhost:9000',
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False  # Not over SSL. Should probably be changed
    )
    # Using Pillow to fetch metadata
    width, height, size, imageFormat, name = fetch_metadata(image)

    serializer = ImageForMinioSerializer(data={
        "name": name,
        "image": image,
        "height": height,
        "width": width,
        "size": size,  # pillow_image.size will return (width, height)
        "path_to_image": "NEEDSTOBESET"
        }
    )

    if serializer.is_valid(raise_exception=True) and is_image(image.content_type):
        # Resetting the cursor to the beginning of the file
        # django-storage-minio takes care of this automatically
        image.file.seek(0)
        etag = minioClient.put_object(
                "anas",
                image.name,
                image.file,
                image.size
            )
        # serializer.save()

        return Response({"response": "serializer is valid"})
    else:
        return Response({"Serializer invalid": serializer.errors})


# *****************************************************************************
# HELPERS
# *****************************************************************************

def is_image(content_type):
    """Determines if the content_type provided refers to an image"""
    if content_type == "image/jpeg" or content_type == "image/png":
        return True
    else:
        return False


def fetch_metadata(image):
    x = Image.open(image)
    return x.width, x.height, x.fp.size, x.format, x.fp.name


# def minio_client():
