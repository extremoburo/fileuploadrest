# *****************************************************************************
# IMPORTS
# *****************************************************************************

# PYTHON

# PIP
from PIL import Image
from minio.error import ResponseError
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import minio


# DJANGO
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# PROJECT
from .imageUpload.serializers import ImageForMinioSerializer
from .imageUpload.serializers import ImageSerializer
from .imageUpload.storage import MinioStoreStorage

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
    image = request.FILES["image_to_upload"]
    serializer = ImageSerializer(data={
        "name": image.name,
        "image": image
        }
    )
    if (
        serializer.is_valid(raise_exception=True) and
        is_image(image.content_type)
    ):
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
    minioClient = create_minio_client_from_settings()
    serializer = ImageSerializer(data={
        "name": image.name,
        "image": image
        }
    )

    if (
        serializer.is_valid(raise_exception=True) and
        is_image(image.content_type)
    ):
        serializer.save()
        # Copying file from disk into a minio bucket
        if(minioClient.bucket_exists("anas")):
            try:
                # serializer.data["image"] is the relative path to the image
                image_path = get_setting("BASE_DIR") + serializer.data["image"]
                minioClient.fput_object("anas", image.name, image_path)
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
    minioClient = create_minio_client_from_settings()

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

    if (
        serializer.is_valid(raise_exception=True) and
        is_image(image.content_type)
    ):
        # Resetting the cursor to the beginning of the file
        # 'django-storage-minio' takes care of this automatically
        image.file.seek(0)
        etag = minioClient.put_object(
                "anas",
                image.name,
                image.file,
                image.size
            )

        return Response({"response": etag})


@api_view(["POST"])
@parser_classes((FormParser, MultiPartParser))
def upload_image_to_minio_package(request):
    """
    Upload image using slightly modified package
    """
    # Instanciating MinioStoreStorage creates a Minio client from settings
    # and a bucket with the name passed to it.
    x = MinioStoreStorage("abdelhalim")
    image = request.FILES["image_to_upload"]
    width, height, size, imageFormat, name = fetch_metadata(image)

    # The name might conflict with an already existing picture
    while x.exists(name):
        name = name + "X"

    # Using Pillow to fetch metadata
    width, height, size, image_format, name = fetch_metadata(image)

    serializer = ImageForMinioSerializer(data={
        "name": name,
        "image": image,
        "height": height,
        "width": width,
        "size": size,  # pillow_image.size will return (width, height)
        "path_to_image": "NEEDSTOBESET",  # See presigned URLs in Minio?
        "image_format": image_format
        }
    )

    if (
        serializer.is_valid(raise_exception=True) and
        is_image(image.content_type)
    ):
        # What if saving does not go well?
        # Wrap in a try/except statement
        x._save(name, image)
        serializer.save()
        return Response({"response": "Picture saved"})


# *****************************************************************************
# HELPERS
# *****************************************************************************


def is_image(content_type):
    """Determines if the content_type provided refers to an image"""
    return content_type == "image/jpeg" or content_type == "image/png"


def fetch_metadata(image):
    x = Image.open(image)
    # I need to set the cursot to the beginning of the image?
    return x.width, x.height, x.fp.size, x.format, x.fp.name


# The foloowing are functions taken from 'django-minio-storage'
# They are not needed in the view upload_image_to_minio_package(request)
# and should be eliminated.


_NoValue = object()


def get_setting(name, default=_NoValue, ):
    result = getattr(settings, name, default)
    if result is _NoValue:
        print("Attr {} : {}".format(name, getattr(settings, name, default)))
        raise ImproperlyConfigured
    else:
        return result


def create_minio_client_from_settings():
    endpoint = get_setting("MINIO_STORAGE_ENDPOINT")
    access_key = get_setting("MINIO_STORAGE_ACCESS_KEY")
    secret_key = get_setting("MINIO_STORAGE_SECRET_KEY")
    secure = get_setting("MINIO_STORAGE_USE_HTTPS", True)
    client = minio.Minio(endpoint,
                         access_key=access_key,
                         secret_key=secret_key,
                         secure=secure)
    return client
