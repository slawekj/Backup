import os
import sys
import shutil
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from io import BytesIO

import click
import piexif
import pillow_heif
from PIL import Image

# Set up rolling logging to log.txt in the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'log.txt')
handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[handler]
)

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
    except Exception as e:
        logging.warning(f"Failed to extract year from EXIF: {e}")
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
              type=click.Path(exists=False, file_okay=False, writable=True),
              required=True,
              help='Output folder to copy the photo to')
def copy_photo(photo_file, photo_name, output_folder):
    try:
        if photo_file == '/dev/stdin':
            data = sys.stdin.buffer.read()
            year = get_photo_year(BytesIO(data))
            src = BytesIO(data)
            logging.info(f"Read photo from stdin, determined year: {year}")
        else:
            year = get_photo_year(photo_file)
            src = open(photo_file, 'rb')
            logging.info(f"Read photo from file {photo_file}, determined year: {year}")
        output_dir = os.path.join(output_folder, year)
        os.makedirs(output_dir, exist_ok=True)
        dst_path = os.path.join(output_dir, photo_name)
        with open(dst_path, 'wb') as dst:
            shutil.copyfileobj(src, dst)
        logging.info(f"Copied photo to {dst_path}")
    except Exception as e:
        logging.error(f"Error copying photo: {e}")
        raise
    finally:
        if photo_file != '/dev/stdin' and 'src' in locals():
            src.close()


if __name__ == '__main__':
    copy_photo()
