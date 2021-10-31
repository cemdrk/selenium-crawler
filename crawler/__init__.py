import dataclasses
import json
import os
import random
import time

from pathlib import Path

import requests

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


from crawler.browser import (
    find_img_path_and_save,
    find_pronunciations_and_save,
    get_browser,
    find_title,
    find_word_class,
    find_definitions,
)
from crawler.helpers import clear_definition_text
from crawler.model import Record


CRAWL_BASE_URL = 'https://dictionary.cambridge.org/'
DICTIONARY_URL_TEMPLATE = f'{CRAWL_BASE_URL}dictionary/english/{{}}/'


def main(input_file, output_file, img_folder, audio_folder):
    words = []
    with open(input_file, encoding='utf8') as f:
        words = [line.rstrip('\n') for line in f.readlines()]

    browser = get_browser()

    records = []

    try:
        for w in words:
            try:
                browser.get(DICTIONARY_URL_TEMPLATE.format(w))

                title = find_title(browser)
                word_class = find_word_class(browser)
                definitions = find_definitions(browser)
                img_path = find_img_path_and_save(browser, img_folder)
                pronunciations = find_pronunciations_and_save(browser, audio_folder)

                record_options = dict(
                    title=title.text,
                    word_class=word_class.text,
                    definitions=[clear_definition_text(_def.text) for _def in definitions[:3]],
                    img=img_path,
                    pronunciations=pronunciations
                )
                rec = Record(**record_options)

                records.append(dataclasses.asdict(rec))
            except NoSuchElementException as ne:
                print(ne)
            except WebDriverException as we:
                print(we)
            except requests.exceptions.ConnectionError as ce:
                print(ce)

            time.sleep(round(random.uniform(1, 1.5), 1))
    finally:
        browser.quit()

    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(records, indent=2, ensure_ascii=False))
