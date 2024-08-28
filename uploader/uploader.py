import io
import json
import tempfile
import time

import boto3
import requests

from base import Settings
from utils import logs, utils

logger = logs.get_logger("mashiro")
S3_CLIENT = boto3.client('s3')

def upload_image_to_s3(image_url, upload_to):
    r = requests.get(image_url)
    if r.status_code != 200:
        logger.info(f"code: {r.status_code}, cant get twi_images")
        return False
    else:
        img_content = io.BytesIO(r.content)
        S3_CLIENT.upload_fileobj(img_content, Settings.BUCKET_NAME , upload_to)
        time.sleep(1)
        is_uploaded = utils.check_file_exists(Settings.BUCKET_NAME, upload_to)

        return is_uploaded

def upload_metadata_to_s3(metadata, upload_to):
    metadata = json.dumps(metadata, ensure_ascii=False)
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as f:
            f.write(metadata)
        S3_CLIENT.upload_fileobj(tf, Settings.BUCKET_NAME, upload_to)

    return None