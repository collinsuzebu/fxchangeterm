import os
# from selenium import webdriver
import requests


class WebRequest:
	def __init__(self, base_url):
		self._base_url = base_url
		self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

		# self._chromedriver_path = os.path.join(os.curdir, 'chromedriver/chromedriver')
		# self._options = webdriver.ChromeOptions()
		# self._options.headless = True
		# self._options.add_argument('--incognito')

		# self._driver = webdriver.Chrome(options=self._options)

	def fetch_data(self):
		url = self._base_url
		self._response = requests.get(url, headers=self._headers)

		if not self._response.ok:
			error_message = (f'Could not connect to ==> {url}')
			raise Exception(error_message)
		return self._response.text




	# def fetch_data(self):
	# 	url = self._base_url
	# 	self._driver.get(url)
	
	# 	if self._driver.title == '404 Not Found':
	# 		error_message = (f'Could not connect to '
	# 			'==>{base_url}')
	# 		raise Exception(error_message)
	# 	self._driver.quit()
	# 	return self._driver.page_source

