from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import base64
#email modules
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def generateEmailMessage(riders):
	message = ''
	for rider in riders:
		message += rider['name'] + ' was on ' + rider['track'] + ', on ' + rider['date'] + ' and spent ' + rider['time'] + ' on the track.' + '\n\tLink to the track: ' + rider['link'] +  '\n\n'
	return message

#handles sending emails
def sendEmailAlert(riders):
	fromaddr = "deanpatrickgaffney@gmail.com"	
	toaddr = fromaddr
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Track has changed!"
	 
	body = generateEmailMessage(riders)

	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, base64.b64decode('bWVnYWRldGgx'))		#email address and password which is encoded
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

#links that need to be looked at.
links = ['https://www.strava.com/segments/10418518','https://www.strava.com/segments/9328740',
'https://www.strava.com/segments/13529167','https://www.strava.com/segments/7860329','https://www.strava.com/segments/8415499',
'https://www.strava.com/segments/8415509']
#list of rider dictionaries
riders = []
rider_entries = {}
login_page = 'https://www.strava.com/login'

driver = webdriver.Firefox()
driver.get(login_page)

email_form = driver.find_element(By.ID,'email')
email_form.send_keys('gaffmasterflex123@gmail.com')

password_form = driver.find_element(By.ID,'password')
password_form.send_keys(base64.b64decode('bWVnYWRldGgx'))		#encrypt password for shoulder surfers
password_form.send_keys(Keys.RETURN)

sleep(2)			#allows time for login page to properly load and allow javascript vars to stay so login is still registered
for link in links:
	driver.get(link)

	#use beautiful soup now to pull down these pages
	#more than likely will need to naviagte through all pages and have a sleep delay between all loads
	html = driver.page_source
	soup = BeautifulSoup(html)
	title = driver.find_element_by_xpath('//span[@data-full-name]').text
	print title
	driver.find_element_by_xpath("//button[@class='btn selection btn-unstyled']").click()	#click button to generate javascript list
	driver.find_element_by_link_text('Today').click()		#click on today to filter for today

	sleep(2)				#sleep to allow javascript to add filter to table
	#grab table
	leaderboard = driver.find_element_by_id('results')
	#get rows in table
	rows = leaderboard.find_elements_by_tag_name('tr')

	print len(rows)		

	#get all columns in that row (going to put this in loop starting at 1 all the way to length)
	#make sure there is an entry
	#!!!!! I NEED A LIST TO HOLD SEPARATE DICTIONARIES FOR EACH RIDER!!!!!!
	index = 1
	while index < len(rows):
		rider_details = {}
		cols = rows[index].find_elements(By.TAG_NAME,'td')
		if cols[0].text == 'No results found':
			break
		print cols[1].text		#rider name
		print cols[2].text		#rider date 
		print cols[7].text      #rider time

		#put entries into dictionary
		rider_details['name'] = cols[1].text
		rider_details['date'] = cols[2].text
		rider_details['time'] = cols[7].text
		rider_details['track']= title
		rider_details['link'] = link
		#add rider to riders list
		riders.append(rider_details)
		index = index + 1

for rider in riders:
	print '%s\t%s\t%s' % (rider['name'],rider['date'],rider['time'])
sleep(2)
driver.quit()

#if riders list is empty no enries were made
if len(riders) == 0:
	print 'No entries today.'
	sleep(2)
	driver.quit()
else:
	#send email
	print 'should send email now.'
	sendEmailAlert(riders)

