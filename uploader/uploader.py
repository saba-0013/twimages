import io
import json
import tempfile

import boto3
import requests

from base import Settings

S3_CLIENT = boto3.client('s3')

def upload_image_to_s3(image_url, upload_to):
    res = requests.get(image_url)
    print(res.status_code)
    img_content = io.BytesIO(res.content)
    S3_CLIENT.upload_fileobj(img_content, Settings.BUCKET_NAME, upload_to)

    return None

def upload_metadata_to_s3(metadata, upload_to):
    metadata = json.dumps(metadata, ensure_ascii=False)
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as f:
            f.write(metadata)
        S3_CLIENT.upload_fileobj(tf, Settings.BUCKET_NAME, upload_to)

    return None