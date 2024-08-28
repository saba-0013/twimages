from urllib.parse import urlparse

import boto3

from utils import logs

logger = logs.get_logger("mashiro")

s3_client = boto3.client('s3')

def extract_twi_status_from_url(url):
    parsed_path = urlparse(url).path.split("/")
    status_code = parsed_path[-1]

    return status_code

def is_url(message) -> bool:
    o = urlparse(message)
    return True if o.scheme and o.netloc else False

def check_file_exists(bucket_name, s3_file_path):
    try:
        r = s3_client.head_object(Bucket=bucket_name, Key=s3_file_path)
        if r["ResponseMetadata"]["HTTPStatusCode"] != 200:
            logger.info(f"code: {r['ResponseMetadata']['HTTPStatusCode']} upload faild. path: {s3_file_path}")
            return False
        elif r["ContentLength"] == 0:
            logger.info(f"upload faild. path: {s3_file_path}")
            return False
        else:
            logger.info(r["ContentLength"])
            return True
    except Exception as e:
        logger.error(e)
        return False
