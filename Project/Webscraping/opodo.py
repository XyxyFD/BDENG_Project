from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import random

# Headless Chrome einrichten
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Optional zur Vermeidung von Bot-Erkennung
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

heute = datetime.now()
timestamp = heute.strftime('%m%d_%H%M')

domains = {
    "at": "https://www.opodo.at/",
    "de": "https://www.opodo.de/",
    "nl": "https://www.opodo.nl/",
    "fr": "https://www.opodo.fr/",
    "pt": "https://www.opodo.pt/",
    "es": "https://www.opodo.es/",
    "it": "https://www.opodo.it/"
}

try:
    for abbr, url in domains.items():
        print(f"Besuche {url}...")
        driver.get(url)
        
        try:
            # Try to find the button using find_elements to avoid NoSuchElementException if not present
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="show-more-less-button"]')
            if buttons: # If the button element is found
                button = buttons[0]
                # Wait for the button to be clickable and attempt to click it
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
                time.sleep(2) # Give some time for content to load after click
                print(" 'Show more/less' button geklickt.")
            else:
                print(" 'Show more/less' button nicht gefunden.")
        except Exception as e:
            # Catch any exception that occurs during the button interaction
            print(f"Fehler bei der Interaktion mit dem 'Show more/less' Button auf {url}: {e}")
            
        # HTML auslesen und in Datei schreiben
        html = driver.page_source
        dateiname = f"Project/Html/opodoHTML/opodo_{abbr}_{timestamp}.html"
        with open(dateiname, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"HTML erfolgreich in {dateiname} gespeichert.")
        time.sleep(random.uniform(5, 10)) # Random delay between domains

finally:
    driver.quit()
    print("Fertig")
