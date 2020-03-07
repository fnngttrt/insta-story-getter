from selenium import webdriver
import time
import urllib.request
import sys
import optparse
import platform
from pathlib import Path
import logging
import os
from selenium.webdriver.remote.remote_connection import LOGGER
from getpass import getpass
LOGGER.setLevel(logging.WARNING)


parser = optparse.OptionParser()
parser.add_option('-a', '--account', action="store", dest="account", help="The instagram account, from which the contents will be downloaded", default="nasa")#
parser.add_option('--private', action="store_true", default=False, help="Add this option, if the user is private")


options, args = parser.parse_args()

name = options.account
insturl = 'https://instagram.com/stories/' + name + '/'

relpath = 'drivers/chromedriver'

path = Path().absolute()
webdriverpath = os.path.join(path, relpath)

def getcred():
	name = input('Your instagram username or email: ')
	password = getpass('Your instagram password: ')


def checkexist():
	global driver
	try:
		driver = webdriver.Chrome(executable_path= webdriverpath)
		driver.get('https://instagram.com/{}'.format(name))
		try:
			assert name in driver.title
		except:
			return False
		else:
			return True
	except:
		print('Can\'t open driver!')

def checkstatus():
	driver.get('https://instagram.com/stories/{}'.format(name))
	try:
		assert 'Stories' in driver.title
	except:
		return False
	else:
		return True

def openacc():
	try:
		driver = webdriver.Chrome(executable_path= webdriverpath)
		driver.get(insturl)
		try:
			assert 'Stories' in driver.title
		except:
			if name in driver.title:
				driver.close()
				print('This instagram account does not have a story!')
				print('Press enter to exit')
				input()
				sys.exit()
			else:
				driver.close()
				print('This instagram acoount does not exist!')
				print('Press enter to exit')
				input()
				sys.exit()

		try:
			user = driver.find_element_by_name("username")
			passwd = driver.find_element_by_name("password")
		except:
			time.sleep(1)
		user.send_keys(username)
		time.sleep(1)
		passwd.send_keys(password)
		try:
			button = driver.find_element_by_css_selector('.L3NKy')
			button.click()
		except:
			pass
		time.sleep(7)
		next = driver.find_element_by_css_selector('.h_zdq')
		next.click()
		time.sleep(1)
		global links
		links = ['None', None]
		global vids
		vids = []
		while True:
			try:
				try:
					#try downloading the image
					#if it fails its a video
					try:
						elem = driver.find_element_by_class_name("y-yJ5")
						url = elem.get_attribute("src")
					except:
						raise Exception
					if url in (None, 'None'):
						raise Exception
					elif url in links:
						nextbuttom = driver.find_element_by_class_name("ow3u_").click()
					else:
						links.append(url)
						print("Got src (IMAGE)")
				except:
					try:
						vids.append(driver.find_element_by_tag_name('source').get_attribute("src"))
						print("Got src (VIDEO)")
					except:
						url = "None"

					if url in links:
						pass
						nextbuttom = driver.find_element_by_class_name("ow3u_").click()
					else:
						links.append(url)
			except:
				#if it cant find anything, the story is over, and the browser exits
				break

			time.sleep(.5)
		driver.close()
		print('Downloading images...')
	except:
		input()
		sys.exit()


def privateacc():
	try:
		try:
			driver = webdriver.Chrome(executable_path= webdriverpath)
		except FileNotFoundError:
			print('Cant find the chromedriver!')
			exit()
		driver.get("https://www.instagram.com/accounts/login/")
		try:
			assert 'Instagram' in driver.title
		except:
			driver.close()
			print('This instagram acoount does not exist!')
			print('Press enter to exit')
			input()
			sys.exit()

		try:
			time.sleep(1.5)
			user = driver.find_element_by_name("username")
			passwd = driver.find_element_by_name("password")
		except:
			time.sleep(1)
			print('Exception')
		user.send_keys(username)
		time.sleep(1)
		passwd.send_keys(password)
		try:
			button = driver.find_element_by_css_selector('.L3NKy')
			button.click()
		except:
			pass
		time.sleep(3)
		notnow = driver.find_element_by_css_selector('.HoLwm').click()
		time.sleep(2)
		driver.get(insturl)
		time.sleep(3)
		try:
			assert "Stories" in driver.title
		except:
			driver.close()
			print('This account hasnt got a story!')
			print('Press enter to exit')
			input()
			sys.exit()
		button = driver.find_element_by_css_selector('.uL8Hv')
		button.click()
		global links
		links = ['None', None]
		global vids
		vids = []
		while True:
			try:
				try:
					#try downloading the image
					#if it fails its a video
					try:
						elem = driver.find_element_by_class_name("y-yJ5")
						url = elem.get_attribute("src")
					except:
						raise Exception
					if url in (None, 'None'):
						raise Exception
					elif url in links:
						nextbuttom = driver.find_element_by_class_name("ow3u_").click()
					else:
						links.append(url)
						print("Got src (IMAGE)")
				except:
					try:
						vids.append(driver.find_element_by_tag_name('source').get_attribute("src"))
						print("Got src (VIDEO)")
					except:
						url = "None"

					if url in links:
						pass
						nextbuttom = driver.find_element_by_class_name("ow3u_").click()
					else:
						links.append(url)
			except:
				#if it cant find anything, the story is over, and the browser exits
				break

			time.sleep(.5)
		driver.close()
		print('Downloading images...')
	except:
		input()
		sys.exit()

print('Please enter your instagram credentials:')
getcred()

print('Checking if user exists...')
if not checkexist():
	print('This user does not exist!')
	exit()

print('Checking if user is public or private')
if not checkstatus():
	print('User is private')

for i in range(0, len(links)):
	if links[i] != None and links[i] != 'None':
		nameimg = name + "\'s story " + str(i) + '.jpg'
		print('Downloading: ' + nameimg)
		currlink = links[i]
		urllib.request.urlretrieve(currlink, nameimg)
		print("Sucess!")
	else:
		pass

print('Downloading videos')
for i in range(0, len(vids)):
	nameimg = name + "\'s story " + str(i) + '.mp4'
	print('Downloading: ' + nameimg)
	currlink = vids[i]
	urllib.request.urlretrieve(currlink, nameimg)
	print("Sucess")

print('Everything has been downloaded!')
print('Press enter to exit')
input()
sys.exit()
