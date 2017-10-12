import requests
from bs4 import BeautifulSoup
from lxml.etree import fromstring
from pyvirtualdisplay import Display
from selenium import webdriver

from settings import *


def try_selenium():
	display = Display(visible=0, size=(800, 600))
	display.start()

	chrome = webdriver.Chrome()
	chrome.get(URL_SHAWN_COMBO)
	elem = chrome.find_element_by_css_selector(
		"#cube-info > div.cube-blockmain > div > div.cube-profits.fn-clear > div:nth-child(3) > div.per")
	result = elem.text
	chrome.quit()
	return result

def try_requests():
	headers = {
		'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
	}
	response = requests.get(URL_SHAWN_COMBO, headers=headers)
	content = response.content
	page = BeautifulSoup(content)
	elem = page.select("#cube-info > div.cube-blockmain > div > div.cube-profits.fn-clear > div:nth-of-type(3) > div.per")[0]
	print(elem.text)


if __name__ == '__main__':
	try_requests()