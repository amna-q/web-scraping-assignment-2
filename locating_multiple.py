import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
query = "laptop"
os.makedirs("data", exist_ok=True)
file = 0
for i in range(1, 10):
    driver.get(
        f"https://www.amazon.com/s?k={query}&page={i}&crid=2NFNV25TJ6CRA&sprefix=laptop%2Caps%2C428&ref=nb_sb_noss_1"
    )

    elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
    print(f"{len(elems)} items found")
    for elem in elems:
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
            f.write(d)
            file += 1

    time.sleep(2)
driver.close()
