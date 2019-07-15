#!python3
import sys 
sys.path.append(r'C:/Users/jerem/Anaconda3/pkgs/selenium-3.141.0-py36he774522_0/Lib/site-packages')
sys.path.append(r'c:/users/jerem/anaconda3/lib/site-packages')
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import os

#start webdriver and open Google
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r'C:/Users/jerem/OneDrive/Summer/WebScraper/chromedriver.exe',options=options)
driver.get('https://www.google.com')

#send inputs to google search
search = driver.find_element_by_name('q')
key = ''
for i in range(1,len(sys.argv)):
    key += sys.argv[i] + ' '
finalKey = key + 'espn'
search.send_keys(finalKey)
search.submit()

#click on first link for ESPN match statistics and summary 
results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3') 
results[0].click()
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

#scrape home/away team names and final score
away = driver.find_element_by_css_selector('.away').text.split()
awayTeam = ''
for i in range(len(away)-1):
    awayTeam += away[i] + ' '
home = driver.find_element_by_css_selector('.home').text.split()
homeTeam = ' '
for i in range(1,len(home)):
    homeTeam += home[i] + ' '
title = awayTeam + '(' + away[-1] + ') ' + 'vs.' + homeTeam + '(' + home[0] + ') '

#scrape date/time of game
sumClick = driver.find_element_by_css_selector('.summary .link-text')
driver.execute_script('arguments[0].click();', sumClick)
driver.implicitly_wait(10)
date = driver.find_element_by_css_selector('.game-date').get_attribute('innerText')

#click on statistics and scrape 
driver.implicitly_wait(10)
statsClick = driver.find_element_by_css_selector('.stats .link-text')
driver.execute_script('arguments[0].click();', statsClick)
driver.implicitly_wait(10)
stats = driver.find_element_by_css_selector('.content').get_attribute('innerText')
#get rid of irrelevant information
s = stats.split()
s = s[2:12] + s[14:]
#formatting statistics
possession = s[1] + '\t\t' + 'Possession' + '\t\t' + s[2]
shot = s[6] + s[7] + '\t\t' + 'Shots(on Goal)' + '\t\t' + s[8] + s[9]
foul = s[10] + '\t\t' + 'Fouls' + '\t\t\t' + s[12]
yellow = s[13] + '\t\t' + 'Yellow Cards' + '\t\t' + s[16]
red = s[17] + '\t\t' + 'Red Cards' + '\t\t' + s[20]
offside = s[21] + '\t\t' + 'Offsides' + '\t\t' + s[23]
corner = s[24] + '\t\t' + 'Corner Kicks' + '\t\t' + s[27]
save = s[28] + '\t\t' + 'Saves' + '\t\t\t' + s[30]
overall = possession + '\n' + shot + '\n' + foul + '\n' + yellow + '\n' + red + '\n' + offside + '\n' + corner + '\n' + save + '\n'

#click on commentary and scrape
commClick = driver.find_element_by_css_selector('.commentary .link-text')
driver.execute_script('arguments[0].click();', commClick)
driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0,300);")
keyClick = driver.find_element_by_css_selector('#gamepackage-soccer-commentary-tabs > article > header > div > a:nth-child(2)')
driver.execute_script('arguments[0].click();', keyClick)
events = driver.find_element_by_css_selector('.match-commentary > .content').get_attribute('innerText')
#formatting commentary
finalEvents = re.sub('\n|\t', '', events).split('.')

#helper function for writing events to file
def addSpace(string):
    if '+' in string:
        return re.sub(r'(\+\d+\')', r'\g<1>:\t',string)
    else:
        return re.sub(r'(\d+\')', r'\g<1>:\t',string)


#output to text file 
os.chdir('C:\\Users\\jerem\\OneDrive\\Summer\\WebScraper')
f = open(key + 'summary.txt', 'w')
line = '___________________________________________________________' 
eventText = ''
for i in range(len(finalEvents)-1):
    if i == 0:
        string = addSpace(finalEvents[i][10:] + '\n\n')
        eventText += string
    else:
        string = addSpace(finalEvents[i] + '\n\n')
        eventText += string
f.write(title + '\n' + date + '\n' +  line + '\n\n' + 'Statistics:\n\n' + overall + line + '\n\n' + 'Key Events:\n\n' + eventText + line)
f.close()

#end task
driver.quit()
