from bs4 import BeautifulSoup

import os
import sys
import json
import requests
import logging

logging.basicConfig(filename="help.log", level=logging.DEBUG)

# TODO: scrape url page of entire startapps link and return a number of "link to homepage" that aren't working

__author__ = "mauridb"

URL_PASSED = sys.argv[1]
logging.info("Url succesfully take..")

def get_data(url):
	content = requests.get(URL_PASSED)
	return content.text
logging.info("Succesfully get content of url page passed as param..")

content_page = get_data(URL_PASSED)
soup = BeautifulSoup(content_page, 'html.parser')
logging.info("Soup succesfully execute..")

list_div = soup.find_all('div', {"class": "topix-item"})
list_url_to_try = [div.find('a')['href'] for div in list_div]
logging.info("Funny, list retrieved succesfully..")

def try_startups_url(list_url):
	"""
	To test get url of single startapp url.

	params:
	-list_url is the retrieved list of url of all startups ready to try
	"""
	logging.info("Test operation RUNNING..")
	result = {
		'error':[],
		'valid':{
			'status_ok':[],
			'othest_status': [],
			},
		'timeout':[]
	}
	for index, link in enumerate(list_url):
		try:
			link = str(link)
		except:
			logging.warning("Ops!! Something has been wrong..")
		
		if link != "#": 
			try:
				response = requests.get(link, timeout=5)
			except:
			# handle timeout exception error
				logging.warning("ConnectionTimeout exception error..")
				result['timeout'].append((index, link, "s% raise a ConnectTimeout exception error.." % link))
			print response
			if response.status_code == 200:
				result['valid']['status_ok'].append((index, link, response.status_code))
			elif response.status_code >= 400:
				result['valid']['othest_status'].append((index, link, response.status_code))
		else:
			result['error'].append((index, link, "Nope, -#- isn\'t a link!"))
	logging.info("Test operation COMPLETED..\n**************\n***************\n")
	return result
	
happy_ending = try_startups_url(list_url_to_try)
# print "##########################\n########################\n##########################\n"
# print happy_ending['error'], len(happy_ending['error'])
# print "##########################\n########################\n##########################\n"
# print happy_ending['valid']['status_ok'], len(happy_ending['valid']['status_ok'])
# print "##########################\n########################\n##########################\n"
# print happy_ending['valid']['othest_status'], len(happy_ending['valid']['othest_status'])
# print "##########################\n########################\n##########################\n"
# print happy_ending['timeout'], len(happy_ending['timeout'])
# print "##########################\n########################\n##########################\n"

