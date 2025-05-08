import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

driver.get("https://gamalytic.com/game-list?columns=capsule%2Cname%2CfirstReleaseDate%2CcopiesSold%2Cprice%2Crevenue%2CavgPlaytime%2CreviewScore%2Creviews%2Cfollowers%2Cwishlists%2CpublisherClass%2Cpublishers%2Cdevelopers%2CwishlistsAtRelease%2Cm1saleWishlistRatio%2Cm1revenue%2Cm1sales%2Cy1revenue%2Cy1sales%2Crevenue2015%2Crevenue2016%2Crevenue2017%2Crevenue2018%2Crevenue2019%2Crevenue2020%2Crevenue2021%2Crevenue2022%2Crevenue2023%2Crevenue2024%2Crevenue2025%2Csales2015%2Csales2016%2Csales2017%2Csales2018%2Csales2019%2Csales2020%2Csales2021%2Csales2022%2Csales2023%2Csales2024%2Csales2025&sort_model=%5B%7B%22field%22%3A%22copiesSold%22%2C%22sort%22%3A%22desc%22%7D%5D")

time.sleep(4)


results = []
page_count = 400
backup_frequency = 20


backups = [f for f in os.listdir() if f.startswith("backup_gamalytic_page_") and f.endswith(".csv")]
if backups:
    latest = max(backups, key=lambda f: int(f.split("_")[-1].split(".")[0]))
    page_count = int(latest.split("_")[-1].split(".")[0])
    results = pd.read_csv(latest).to_dict(orient="records")
    print(f"🔁 Resuming from page {page_count} using {latest}")

    
    for i in range(page_count):
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Go to next page']")
            if next_button.is_enabled():
                next_button.click()
                time.sleep(3)
        except NoSuchElementException:
            print("❌ Failed to resume to page. Check if site changed.")
            driver.quit()
            exit()
else:
    print("🆕 Starting fresh scrape.")


while True:
    print(f"📄 Scraping page {page_count + 1}")

    try:
        scroll_container = driver.find_element(By.CLASS_NAME, "MuiDataGrid-virtualScroller")
        for i in range(10):
            driver.execute_script("arguments[0].scrollTop += 150", scroll_container)
            time.sleep(0.3)
    except Exception as e:
        print(f"Scroll error: {e}")
        break

    rows = driver.find_elements(By.CSS_SELECTOR, "div.MuiDataGrid-row")
    for row in rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, "div[data-field='name'] a").text
            game_class = row.find_element(By.CSS_SELECTOR, "div[data-field='publisherClass']").text
            developer = row.find_element(By.CSS_SELECTOR, "div[data-field='developers']").text
            copies_sold = row.find_element(By.CSS_SELECTOR, "div[data-field='copiesSold']").text

            results.append({
                "name": name,
                "developer": developer,
                "class": game_class,
                "copies_sold": copies_sold
            })
        except NoSuchElementException:
            continue

    
    if page_count % backup_frequency == 0 and page_count > 0:
        df_partial = pd.DataFrame(results).drop_duplicates()
        df_partial.to_csv(f"backup_gamalytic_page_{page_count}.csv", index=False)
        print(f"💾 Backup saved at page {page_count}")

    
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Go to next page']")
        if not next_button.is_enabled():
            print("✅ Reached final page.")
            break
        next_button.click()
        time.sleep(3)
        page_count += 1
    except NoSuchElementException:
        print("⚠️ No 'Next' button found — exiting.")
        break

driver.quit()
df = pd.DataFrame(results).drop_duplicates()
df.to_csv("gamalytic_full_dataset.csv", index=False)
print(f"✅ Scraping complete. Total pages scraped: {page_count + 1}")
print("📁 Saved to 'gamalytic_full_dataset.csv'")