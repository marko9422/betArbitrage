import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# This return text without special signs.
from unidecode import unidecode
from datetime import datetime

from database import save_data
from database import delete_all_data

# Keep open chrome.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open url.
driver.get('https://www.ifortuna.sk/stavkovanie/basketbal')
driver.maximize_window()
time.sleep(1)

# Press cookie button.
driver.find_element(By.XPATH, '//*[@id="cookie-consent-button-accept"]').click()
time.sleep(1)

# function from database.py which delete all rows from table.
delete_all_data('fortuna')

# Tick hide live data.
driver.find_element(By.XPATH, '//*[@id="checkbox_live_disabled"]').click()

# Scroll to the bottom.
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
js_code_scrollTop = "window.scrollTo(0, 0);"
driver.execute_script(js_code_scrollTop)
time.sleep(1)


# Change data to winner ,click with javascript.
viac_button = driver.find_elements(
    By.XPATH, "//div[@class='show-more']")

for one in viac_button:
    one.click()

js_code_click = """
var divElement = document.getElementsByClassName('facet-filters');
Array.from(divElement).forEach(element => {
    var childElement = element.children[2];
    var grandchildren = childElement.children;
    grandchildren[0].click();
});
"""
driver.execute_script(js_code_click)

# Get data.

matches = []
dates = []
odds = []

all_divs = driver.find_elements(By.XPATH, "//div[@class='market-with-header']")

for i in range(len(all_divs)):
    soup = BeautifulSoup(all_divs[i].get_attribute('innerHTML'), 'html.parser')
    time = soup.select('div div.right span.datetime')
    match = soup.select('div a.names')
    odds_all = soup.select('div.market div.odds div.odds-group a')

    # # get date and time
    for one in time:
        # Get current year.
        current_year = datetime.now().year
        # Save date and time into dates array with correct form.
        time_text = one.text.replace(' ', '').replace('\n', '')
        split_string = time_text.split('.')
        date = f'{split_string[0]}.{split_string[1]}.{current_year} {split_string[2]}'
        date_obj = datetime.strptime(date, '%d.%m.%Y %H:%M')
        new_date_str = datetime.strftime(date_obj, '%d.%m.%y %H:%M')
        dates.append(new_date_str)

    # # get match.
    for one in match:
        match_text = one.text.strip()
        matches.append(match_text)
        odd = soup.select('div.market div.odds div.odds-group a span.odds-value')

        odds_between = []
        # Get odds in array
        if len(odd) == 2:
            odds_between.append(odd[0].text)
            odds_between.append(odd[1].text)
        odds.append(odds_between)

for i in range(len(matches)):
    # Editing matches text.
    match_trasformed = unidecode(matches[i].upper())
    match_splitted = match_trasformed.split(' ')

    # Editing odds.
    odds[i].insert(0, '1')
    odds[i].insert(2, '2')

    if len(odds[i]) == 4: # If odd contain 0 odds do not save.
        save_data('fortuna', 'basketball_fortuna', json.dumps(match_splitted), dates[i], json.dumps(odds[i]))

print('Sucess fortuna')

