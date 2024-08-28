import csv
import time
from datetime import datetime, timedelta
from pathlib import Path

import discord

from base import Envs, Settings
from twimage import twimage
from utils import logs, utils

logger = logs.get_logger("mashiro")

FILE_PATH = Path(Settings.FILE_PATH)

# discord settings
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel = client.get_channel(Envs.CHANNEL_ID)
    # ref: https://discordpy.readthedocs.io/ja/latest/api.html#discord.abc.Messageable.history
    # messages = [m.content async for m in channel.history(limit=100)]
    messages = [m.content async for m in channel.history(limit=None)]

    urls = list(filter(lambda x: utils.is_url(x), set(messages)))
    twi_codes = list(set(map(utils.extract_twi_status_from_url, urls)))

    logger.info(f"urls: {len(urls)}")
    logger.info(f"unique_len: {len(twi_codes)}")

    urls = [{"url": urls[i]} for i in range(len(urls))]

    with open(FILE_PATH, mode="w", newline="") as f:
        writer_ = csv.DictWriter(f, fieldnames=["url"])
        writer_.writeheader()
        writer_.writerows(urls)

    await client.close()


client.run(Envs.CLIENT_TOKEN)

with open(FILE_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    urls = [row["url"] for row in reader]

for idx, url in enumerate(urls):
    try:
        uploaded_ = twimage(url)
        if not uploaded_:
            logger.info(f"upload failed: {url}")
        else:
            logger.info(f"success, {idx}")
        time.sleep(0.5)
    except Exception as e:
        logger.error(e)
        logger.info(url)