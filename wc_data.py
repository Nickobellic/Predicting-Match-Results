from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re
import pandas as pd

CHROME_URL = "E:\chromedriver-win64\chromedriver.exe"

driver = Chrome(service=Service(CHROME_URL))

driver.get("http://www.howstat.com/cricket/Statistics/WorldCup/SeriesStats.asp?SeriesCode=0459")



countries = set()
home = []
away = []
winners = []
new_tables = driver.find_element(By.XPATH,
                             f"/html/body/table/tbody/tr/td[2]/table[3]/tbody/tr/td[1]/table/tbody")

print(len(new_tables.text.split("\n"))+1)
for i in range(2, len(new_tables.text.split("\n")) - 1):
    tables = driver.find_element(By.XPATH, f"/html/body/table/tbody/tr/td[2]/table[3]/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[3]")
    home.append(tables.text.split(" v ")[0])
    away.append(tables.text.split(" v ")[1])
    for versus in range(2):
        countries.add(tables.text.split(" v ")[versus])
countries = list(countries)
countries.extend(["abandoned", "result", "tied"])
for i in range(2, 50):
    results = driver.find_element(By.XPATH,
                                  f"/html/body/table/tbody/tr/td[2]/table[3]/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[5]")

    for country in countries:
        winner = re.findall(country, results.text)
        if len(winner) != 0:
            winners.append(winner[0])


wc_data = pd.DataFrame({"Home_Team": home, "Away_Team": away, "Winner": winners})
wc_data.to_csv("ICC_CWC_1999.csv")
