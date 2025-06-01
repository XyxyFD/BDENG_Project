from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
# Headless Chrome einrichten
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("window-size=1920,1080")

heute = datetime.now()
timestamp = heute.strftime('%m%d_%H%M')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

try:
    # Seite laden
    driver.get("https://www.opodo.at/")


    
    button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="show-more-less-button"]').click()
    
    # HTML sofort auslesen und in Datei schreiben
    container = driver.find_elements(
        By.CSS_SELECTOR,
        "div.css-1upemms.e17fzqxg0"
    )
    print(f"Gefundene Angebots-Container: {len(container)}")


    html = driver.page_source
    with open(f"Project/Html/opodoHTML/opodo_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML erfolgreich in opodo_{timestamp}.html gespeichert.")
    
finally:
    driver.quit()
