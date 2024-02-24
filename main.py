from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

CHROME_URL = "E:\chromedriver-win64\chromedriver.exe"

driver = Chrome(service=Service(CHROME_URL))
driver.maximize_window()


driver.get("https://signal.nfx.com/investor-lists/top-legaltech-pre-seed-investors")

data = []

def get_investors_data(i):
    INVESTORS_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[1]/div/div[2]/div/div/a/strong"

    # get URL too
    COMPANY_NAME_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[1]/div/div[2]/div/a"
    ROLE_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[1]/div/div[2]/div/span"
    SWEET_SPOT_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[3]/div/div[1]"
    RANGE_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[3]/div/div[2]"
    LOCATION_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[4]/div/div/div/div/span"
    SEE_MORE_LOCATION_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[4]/div/div/span"
    SEE_MORE_CATEGORIES_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[5]/div/div/span"
    CATEGORIES_XPATH = f"/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/table/tbody/tr[{i}]/td[5]/div/div/div/div"
    LOAD_XPATH = "/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/button"

    investor_name = driver.find_element(By.XPATH, INVESTORS_XPATH).text
    company = driver.find_element(By.XPATH, COMPANY_NAME_XPATH)
    company_name = company.text
    company_url = company.get_attribute("href")
    role = driver.find_element(By.XPATH, ROLE_XPATH).text
    sweet_spot = driver.find_element(By.XPATH, SWEET_SPOT_XPATH).text
    range_name = driver.find_element(By.XPATH, RANGE_XPATH).text
    try:
        see_more_location = driver.find_element(By.XPATH, SEE_MORE_LOCATION_XPATH)
        see_more_location.click()
        time.sleep(2)
        location_name = driver.find_element(By.XPATH, LOCATION_XPATH).text
    except NoSuchElementException:
        location_name = driver.find_element(By.XPATH, LOCATION_XPATH).text

    try:
        see_more_category = driver.find_element(By.XPATH, SEE_MORE_CATEGORIES_XPATH)
        see_more_category.click()
        time.sleep(2)
        categories_name = driver.find_element(By.XPATH, CATEGORIES_XPATH).text
    except NoSuchElementException:
        categories_name = driver.find_element(By.XPATH, CATEGORIES_XPATH).text

    dictionary = {
        "Investors": investor_name,
        "Company Name": company_name,
        "Company URL": company_url,
        "Role": role,
        "Sweet Spot": sweet_spot,
        "Range": range_name,
        "Location": location_name,
        "Categories": categories_name,
    }
    print(dictionary)
    data.append(dictionary)



time.sleep(5)
for i in range(1, 241):
    try:
        get_investors_data(i)
        if i % 8 == 0:
            LOAD_DATA = "/html/body/div[1]/div/div/main/div[1]/div[1]/div[2]/button"
            load = driver.find_element(By.XPATH, LOAD_DATA)
            load.click()
            time.sleep(4)

    except NoSuchElementException:
        action = ActionChains(driver)
        action.scroll_by_amount(delta_x=0, delta_y=1000).perform()

df = pd.DataFrame(data=data).to_csv("Signal_NFX_data.csv")

time.sleep(5)