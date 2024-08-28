import os
from dataclasses import dataclass


@dataclass
class Envs:
    CHANNEL_ID = int(os.environ["CHANNEL_ID"])
    CLIENT_TOKEN = os.environ["CLIENT_TOKEN"]

@dataclass
class Settings:
    BUCKET_NAME = "twi-images"
    # FOLDER_NAME = "monochrome"
    FOLDER_NAME = "illust"
    FILE_PATH = "./urls.csv"