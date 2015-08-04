#!/usr/bin/env python

# ---
# ---
# ---

import argparse

parser = argparse.ArgumentParser(description='SecApps tool executor')

parser.add_argument('tool', metavar='tool', type=str, choices=['foundation', 'scanner', 'recon', 'wpscanner'], help='the tool to be executed')
parser.add_argument('target', metavar='target', type=str, help='the target to be tested')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug messages')
parser.add_argument('-r, ''--report-format', dest='report_format', type=str, choices=['csv', 'xml', 'html', 'json'], default=['html'], nargs='+', help='report format')
parser.add_argument('-a', '--access-token', dest='access_token', type=str, help='access token')
parser.add_argument('-b', '--display-backend', dest='display_backend', type=str, choices=['vnc'], default='', help='display backend')

args = parser.parse_args()

# ---
# ---
# ---

if args.debug:
	import logging
	
	logging.basicConfig(level=logging.DEBUG)
	
# ---
# ---
# ---

from pyvirtualdisplay import Display

if args.display_backend == 'vnc':
	display = Display(backend='xvnc')
	
else:
	display = Display()
	
display.start()

# ---
# ---
# ---

import os
import sys

# ---

from time import sleep

# ---

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ---
# ---
# ---

profile = webdriver.FirefoxProfile()

profile.add_extension(extension='/tmp/websecurify-5.5.0-fx.xpi')

profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/output')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,application/xml,application/html,application/json')

# ---
# ---
# ---

browser=webdriver.Firefox(firefox_profile=profile)

browser.get('https://secapps.com/apps/' + args.tool + '/' + ('access-token=' + args.access_token if args.access_token else ''))

# ---
# ---
# ---

def scanner():
	browser.find_element_by_id('scan-url').send_keys(args.target, Keys.RETURN)
	browser.find_element_by_id('scan-confirmation-label').click()
	browser.find_element_by_id('scan-proceed').click()
	
	# ---
	
	while True:
		status = browser.find_element_by_id('scan-status').text
		
		sys.stdout.write('[*] ' + status + '\n')
		sys.stdout.flush()
		
		# ---
		
		if status.find('100%') > 0:
			break
			
		sleep(5)
		
	# ---
	
	ActionChains(browser).move_to_element(browser.find_element_by_id('toolbar-item-report')).perform()
	
	# ---
	
	for rf in args.report_format:
		print '[*] exporting to', rf
		
		# ---
		
		browser.find_element_by_id('toolbar-item-export-' + rf).click()
		
	# ---
	
	fls = os.listdir('/output')
	
	if len(fls) == 0:
		sys.stdout.write('[-] no reports generated\n')
		sys.stdout.flush()
		
	else:
		for fl in fls:
			sys.stdout.write('[*] report ' + fl + ' generated\n')
			sys.stdout.flush()
			
# ---
# ---
# ---

if __name__ == '__main__':
	{
		'foundation': scanner,
		'scanner': scanner,
		'recon': scanner,
		'wpscanner': scanner
	}.get(args.tool)()
	
# ---
