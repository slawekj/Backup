import os
import sys
import shutil
from datetime import datetime
from io import BytesIO

import click
import piexif
import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()


def get_photo_year(photo_stream):
    try:
        with Image.open(photo_stream) as img:
            exif_data = img.info.get('exif')
            if exif_data:
                exif_dict = piexif.load(exif_data)
                date_bytes = exif_dict['0th'].get(piexif.ImageIFD.DateTime)
                if date_bytes:
                    return str(datetime.strptime(date_bytes.decode(), "%Y:%m:%d %H:%M:%S").year)
    except Exception:
        pass
    return "Others"


@click.command()
@click.option('--photo-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              default='/dev/stdin',
              show_default=True,
              help='Input photo file (default: read from stdin)')
@click.option('--photo-name',
              type=str,
              required=True,
              help='Output photo file name')
@click.option('--output-folder',
              type=click.Path(exists=True, file_okay=False, writable=True),
              required=True,
              help='Output folder to copy the photo to')
def copy_photo(photo_file, photo_name, output_folder):
    if photo_file == '/dev/stdin':
        data = sys.stdin.buffer.read()
        year = get_photo_year(BytesIO(data))
        src = BytesIO(data)
    else:
        year = get_photo_year(photo_file)
        src = open(photo_file, 'rb')
    output_dir = os.path.join(output_folder, year)
    os.makedirs(output_dir, exist_ok=True)
    dst_path = os.path.join(output_dir, photo_name)
    with open(dst_path, 'wb') as dst:
        shutil.copyfileobj(src, dst)
    if photo_file != '/dev/stdin':
        src.close()


if __name__ == '__main__':
    copy_photo()
