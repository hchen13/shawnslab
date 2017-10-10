from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from settings import *

if __name__ == '__main__':
	display = Display(visible=0, size=(800, 600))
	display.start()

	chrome = webdriver.Chrome()
	chrome.get(URL_SHAWN_COMBO)
	elem = chrome.find_element_by_css_selector("#cube-info > div.cube-blockmain > div > div.cube-profits.fn-clear > div:nth-child(3) > div.per")
	print(elem.text)
	sleep(2)
	chrome.quit()