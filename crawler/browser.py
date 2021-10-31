from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from crawler.helpers import download_from_url

_xpath_title = "//span[@class='hw dhw']"
_xpath_posgram = "//span[@class='pos dpos']"
_xpath_definitions = "//div[@class='def ddef_d db']"
_xpath_img = ".//img[@class='i-amphtml-fill-content i-amphtml-replaced-content']"
_xpath_img_div = "//div[@class='dimg']"

_xpath_audio_container = "//span[@class='daud']"
_xpath_audio = ".//source"


def find_elements_by_xpath(driver, _xpath):
    return driver.find_elements(By.XPATH, _xpath)


def find_element_by_xpath(driver, _xpath):
    return driver.find_element(By.XPATH, _xpath)


def find_inside_element_by_xpath(element, _xpath):
    return element.find_element(By.XPATH, _xpath)


def find_inside_elements_by_xpath(element, _xpath):
    return element.find_elements(By.XPATH, _xpath)


def get_browser():
    options = Options()
    options.headless = True
    service = Service(executable_path='./geckodriver')
    browser = webdriver.Firefox(options=options, service=service)

    return browser


def find_title(browser):
    return find_element_by_xpath(browser, _xpath_title)


def find_word_class(browser):
    return find_element_by_xpath(browser, _xpath_posgram)


def find_definitions(browser):
    return find_elements_by_xpath(browser, _xpath_definitions)


def find_img_path_and_save(browser, img_folder):
    try:
        div_img = find_element_by_xpath(browser, _xpath_img_div)
        img = find_inside_element_by_xpath(div_img, _xpath_img)
        img_src = img.get_attribute("src")
        clear_img_src = img_src.split("?")[0].split('/')[-1]
        img_path = f'{img_folder}/{clear_img_src}'
        download_from_url(img_src, img_path)
        return img_path
    except NoSuchElementException as e:
        print('error in images')
        print(e)


def find_pronunciations_and_save(browser, audio_folder):
    try:
        pronunciations = find_elements_by_xpath(browser, _xpath_audio_container)
        cleared_audio_links = []
        for pronunciation in pronunciations:
            audio_sources = find_inside_elements_by_xpath(pronunciation, _xpath_audio)
            audio_links = []
            for audio_source in audio_sources:
                if audio_source.get_attribute("type") == "audio/mpeg":
                    audio_links.append(audio_source.get_attribute("src"))

            for link in audio_links:
                clear_audio_src = link.split("?")[0].split('/')[-1]
                audio_path = f'{audio_folder}/{clear_audio_src}'
                download_from_url(link, audio_path)
                cleared_audio_links.append(audio_path)
        return cleared_audio_links
    except NoSuchElementException as e:
        print('error in pronunciations')
        print(e)
