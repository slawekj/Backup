import os
import shutil
from datetime import datetime

import click
import piexif
import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()


def _photo_file_to_prefix(photo_file):
    try:
        with Image.open(photo_file) as img:
            exif_data = img.info.get('exif')
            if exif_data:
                exif_dict = piexif.load(exif_data)
                date_bytes = exif_dict['0th'].get(piexif.ImageIFD.DateTime)
                if date_bytes:
                    dt = datetime.strptime(date_bytes.decode(), "%Y:%m:%d %H:%M:%S")
                    return f"{dt.year}"
    except Exception:
        pass
    return "Others"


@click.command()
@click.option('--photo-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              required=True,
              help='Input photo file')
@click.option('--output-folder',
              type=click.Path(exists=True, file_okay=False, writable=True),
              required=True,
              help='Output folder to copy the photo to')
def copy_photo(photo_file, output_folder):
    """Copy a photo to the specified output folder and print info."""
    output_dir = os.path.join(output_folder, _photo_file_to_prefix(photo_file))
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy(photo_file, os.path.join(output_dir, os.path.basename(photo_file)))


if __name__ == '__main__':
    copy_photo()
