import json

import requests


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
