import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# This return text without special signs.
from unidecode import unidecode
# Functions created.
from database import save_data
from database import delete_all_data

# Keep open chrome.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open url and press allow essential cookies.
driver.get('https://tipkurz.etipos.sk/zapasy/5?categoryId=5')
driver.maximize_window()
time.sleep(1)

# Handle cookies.
driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
time.sleep(1)

# function from database.py which delete all rows from table.
delete_all_data('tipos')

# Scroll to the bottom.
driver.execute_script('document.querySelector("#event-list > div.simplebar-scroll-content").scrollTop=700000')
time.sleep(1)
driver.execute_script('document.querySelector("#event-list > div.simplebar-scroll-content").scrollTop=700000')
time.sleep(1)
driver.execute_script('document.querySelector("#event-list > div.simplebar-scroll-content").scrollTop=700000')
time.sleep(1)
driver.execute_script('document.querySelector("#event-list > div.simplebar-scroll-content").scrollTop=700000')
time.sleep(1)
driver.execute_script('document.querySelector("#event-list > div.simplebar-scroll-content").scrollTop=700000')
time.sleep(1)

# get all matches into array.
matches = driver.find_elements(By.XPATH, "//div[@class='match-label d-inline']")
dates = driver.find_elements(By.XPATH, "//div[@class='v-center date-col pt-3']")
odds = driver.find_elements(By.XPATH, "//div[@class='flex-nowrap odds-col align-items-center no-gutters row']")

# Data which I want to save into SQL
basketball_data = []
all_matches_odds = []


# func to save data into dictionary.
def add_match(match, date_time, all_odds):
    match_split = match.split(' ')
    new_data = {"match": match_split, "date_time": date_time, "odds": all_odds}
    basketball_data.append(new_data)
    # Reformate Date and time.
    date_without_br = date_time.replace('<br>', ' ')
    # Save into database function.
    save_data('tipos', 'basketball_tipos', json.dumps(match_split), date_without_br, json.dumps(all_odds))
    print('sucess tipos')


# Print data.
for i in range(len(matches)):
    soup = BeautifulSoup(odds[i].get_attribute('innerHTML'), 'html.parser')
    odds_for_match = []
    # Get div div div. that is odds
    div = soup.select('div div div')

    # push data data.
    for one in div:
        odd = one.get_text()
        odds_for_match.append(odd)
    all_matches_odds.append(odds_for_match)
    add_match(unidecode(matches[i].get_attribute('innerHTML').upper()),
              dates[i].get_attribute('innerHTML'), all_matches_odds[i])

print('sucess tipos')