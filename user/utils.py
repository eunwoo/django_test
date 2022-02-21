import base64
import io
import secrets
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile


def decodeDesignImage(data, id):
    try:
        data = base64.b64decode(data.split(",")[1].encode("UTF-8"))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        return InMemoryUploadedFile(
            img_io,
            field_name=None,
            name=id + secrets.token_hex(nbytes=16) + ".jpg",  # 안전한 난수 생성
            content_type="image/jpeg",
            size=img_io.tell,
            charset=None,
        )
    except:
        return None
