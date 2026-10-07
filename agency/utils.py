import os
import io
from pathlib import Path
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings


def compress_and_convert_to_webp(image_file, max_width=1920, max_height=1920, quality=85):
    """
    State-of-the-art image compression & conversion algorithm.
    - Preserves EXIF orientation
    - Converts CMYK/palette to RGB/RGBA
    - Resizes high-res/raw camera uploads smoothly with LANCZOS resampling
    - Encodes to WebP format with optimal compression (85% quality)
    - Returns an InMemoryUploadedFile ready to be saved to Cloudinary or FileSystemStorage
    """
    if not image_file:
        return None

    # Open image
    img = Image.open(image_file)

    # Correct EXIF rotation (e.g. smartphone camera orientation)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Handle color modes
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        # Keep transparency
        img = img.convert('RGBA')
    elif img.mode == 'CMYK':
        img = img.convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Downscale if larger than maximum bounds while maintaining aspect ratio
    orig_w, orig_h = img.size
    if orig_w > max_width or orig_h > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # Save to WebP in memory
    buffer = io.BytesIO()
    img.save(
        buffer,
        format='WEBP',
        quality=quality,
        method=6,  # Highest compression effort
        optimize=True
    )
    buffer.seek(0)

    # Generate new filename with .webp extension
    orig_name = getattr(image_file, 'name', 'upload.jpg')
    base_name = Path(orig_name).stem
    new_filename = f"{base_name}.webp"

    return InMemoryUploadedFile(
        file=buffer,
        field_name='image',
        name=new_filename,
        content_type='image/webp',
        size=buffer.getbuffer().nbytes,
        charset=None
    )
