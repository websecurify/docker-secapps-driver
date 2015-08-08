#!/usr/bin/env python

# ---
# ---
# ---

import argparse

parser = argparse.ArgumentParser(description='SecApps Driver')

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

import logging

if args.debug:
	logging.basicConfig(level=logging.DEBUG)
	
# ---
# ---
# ---

import os
import sys

# ---
# ---
# ---

from pyvirtualdisplay import Display

if args.display_backend == 'vnc':
	display = Display(backend='xvnc')
	
else:
	display = Display()
	
display.start()

if args.display_backend == 'vnc':
	os.system('/usr/bin/fluxbox -display :%s &' % display.display)
	
# ---
# ---
# ---

from time import sleep

# ---

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ---
# ---
# ---

mimes = [
	'application/octet-stream',
	'application/csv',
	'text/csv'
	'application/xml',
	'text/xml'
	'application/html',
	'text/html',
	'application/json',
	'text/json'
]

mimes += ['data:%s' % mime for mime in mimes]

# ---
# ---
# ---

profile = webdriver.FirefoxProfile()

profile.add_extension(extension='/tmp/websecurify-5.5.0-fx.xpi')

profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.helperApps.alwaysAsk.force', False)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/output')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ','.join(mimes))

# ---
# ---
# ---

browser=webdriver.Firefox(firefox_profile=profile)

browser.maximize_window()

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
		
		# ---
		
		sys.stdout.write('[*] ' + status + '\n')
		sys.stdout.flush()
		
		# ---
		
		if status.find('100%') > 0:
			break
			
		# ---
		
		sleep(5)
		
	# ---
	
	chain = ActionChains(browser)
	
	# ---
	
	chain.move_to_element(browser.find_element_by_id('toolbar-item-report')).perform()
	
	for rf in args.report_format:
		chain.move_to_element(browser.find_element_by_id('toolbar-item-export-' + rf)).click().perform()
		
		# ---
		
		sleep(1)
		
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
	try:
		# Navigate to the selected tool, optionaly using the provided token.
		
		browser.get('https://secapps.com/apps/' + args.tool + '/' + ('?access-token=' + args.access_token if args.access_token else ''))
		
		# ---
		
		# Get rid of any automatic popups such as help and welcome screens.
		
		browser.execute_script('document.location.hash = "#"')
		
		# ---
		
		# Sleep for a bit to ensure that the environment is ready.
		
		sleep(5)
		
		# ---
		
		# Execute selenium script based on the selected tool.
		
		{
			'foundation': scanner,
			'scanner': scanner,
			'recon': scanner,
			'spider': scanner,
			'wpscanner': scanner
		}.get(args.tool)()
		
	except (KeyboardInterrupt, SystemExit): pass
	
# ---
