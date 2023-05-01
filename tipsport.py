import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# This return text without special signs.
from datetime import datetime
from unidecode import unidecode

from database import save_data
from database import delete_all_data

# Keep open chrome.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open url.
driver.get('https://www.tipsport.sk/kurzy/basketbal-7?matchViewFilters=WINNER_FINAL_DECISION-7&limit=125')
driver.maximize_window()
time.sleep(1)

# Scroll to the bottom.
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)

# function from database.py which delete all rows from table.
delete_all_data('tipsport')

# Get game name.
matches = driver.find_elements(By.XPATH, '//span[@class="o-matchRow__matchName"]')
dates = driver.find_elements(By.XPATH, "//div[@class='o-matchRow__middle']")
odds = driver.find_elements(By.XPATH, "//div[@class='m-matchRowOdds m-matchRowOdds--countOpp2']")

all_matches_odds = []

for i in range(len(matches)):
    soup = BeautifulSoup(odds[i].get_attribute('innerHTML'), 'html.parser')
    odds_for_match = []
    odd_for_match = []

    soup_dates = BeautifulSoup(dates[i].get_attribute('innerHTML'), 'html.parser')
    div_dates = soup_dates.select('div')
    span_dates = soup_dates.select('span')
    # Reformat date.
    date_str = span_dates[0].text
    date = datetime.strptime(date_str, '%d.%m.%Y')
    formatted_date_str = date.strftime('%d.%m.%y')
    dates_data = f"{formatted_date_str} {span_dates[1].text}"

    div = soup.select('div')
    odds_for_match.append(div)
    for one in div:
        odd = one.get_text()
        odd_for_match.append(odd)
    odd_for_match.insert(0, '1')
    odd_for_match.insert(2, '2')
    all_matches_odds.append(odd_for_match)

    # Transform and split matches before save into SQL.
    match_trasformed = unidecode(matches[i].text.upper())
    match_splitted = match_trasformed.split(' ')

    # Function to save game.
    save_data('tipsport', 'basketball_tipsport', json.dumps(match_splitted), dates_data,
              json.dumps(all_matches_odds[i]))

print('sucess tipsport')
