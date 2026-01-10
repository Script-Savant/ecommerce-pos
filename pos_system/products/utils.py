from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
import os

def resize_image(image, size=(800,800), quality=85):
    img = Image.open(image)
    img = img.convert("RGB")
    img.thumbnail(size)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality)

    return ContentFile(buffer.getvalue(), image.name)

def product_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("products", str(instance.product.id), filename)