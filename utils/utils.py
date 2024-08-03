import io
import json
from urllib.parse import urlparse

import boto3
import requests

from base import Settings

s3_client = boto3.client('s3')

def get_metadata_from_url(url):
    parsed_path = urlparse(url).path.split("/")
    user_id = parsed_path[1]
    status_code = parsed_path[-1]

    # return {"user_id": user_id, "status_code": status_code}
    return user_id, status_code


def get_resources_from_status_code(twi_status):
    url_ = f"https://api.vxtwitter.com/Twitter/status/{twi_status}"
    r = requests.get(url_)
    if r.status_code != 200:
        print(r.status_code)
        return None
    else:
        response_ = json.loads(r.text)
        media_urls = response_.get("mediaURLs", None)
        twi_text = response_.get("text", None)
        twi_date = response_.get("date", None)

    return {"media_urls": media_urls,"twi_text": twi_text, "twi_date": twi_date}

def upload_image_to_s3(image_url, file_name):
    res = requests.get(image_url)
    print(res.status_code)
    img_content = io.BytesIO(res.content)
    s3_client.upload_fileobj(img_content, Settings.BUCKET_NAME, file_name)

    return None

def upload_metadata_to_s3(metadata, upload_to):

    
    return None