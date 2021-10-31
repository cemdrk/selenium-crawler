import os
import requests

from pathlib import Path


def download_from_url(url, output_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }
    try:
        img_data = requests.get(url, headers=headers, timeout=5).content
    except requests.exceptions.ConnectTimeout:
        print('timeout', url)
        return

    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as handler:
        handler.write(img_data)


def clear_definition_text(def_text):
    if def_text[-1] == ':':
        return def_text[:-1]
    return def_text
