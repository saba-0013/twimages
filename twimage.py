import boto3

from base import Settings
from downloader import downloader
from uploader import uploader
from utils import logs, utils

logger = logs.get_logger("mashiro")

S3_CLIENT = boto3.client('s3')
FOLDER_NAME = Settings.FOLDER_NAME

def twimage(url):
    status_code = utils.extract_twi_status_from_url(url)

    # メタデータの取得
    resources_ = downloader.get_resources_from_status_code(status_code)
    resources_["status_code"] = status_code

    file_prefix = f"{FOLDER_NAME}/{resources_['twi_user_id']}/{status_code}"

    checks_ = []
    if not resources_["media_urls"]:
        logger.info(f"resources not exists, {resources_['twi_user_id']}/{status_code}")
        return None
    else:
        # 画像の保存
        for image_index, media_url in enumerate(resources_["media_urls"]):
            file_name = f"{file_prefix}/{image_index}.png"
            is_uploaded = uploader.upload_image_to_s3(media_url, file_name)
            checks_.append(is_uploaded)

        # メタデータの保存
        uploader.upload_metadata_to_s3(resources_, f"{file_prefix}/meta.json")

        return all(checks_)
