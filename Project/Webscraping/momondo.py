from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import random

# Aktuelles Datum für Dateinamen generieren
heute = datetime.now()


iata_codes = [
    "IST",  # Instanbul, Türkei
    "BER",  # Berlin, Deutschland
    "LHR",  # London, Vereinigtes Königreich
    "CDG",  # Paris, Frankreich
    "FCO",  # Rom, Italien
    "MAD",  # Madrid, Spanien
    "KBP",  # Kiew, Ukraine
    "WAW",  # Warschau, Polen
    "OTP",  # Bukarest, Rumänien
    "AMS",  # Amsterdam, Niederlande
    "ARN",  # Stockholm, Schweden
    "BRU",  # Brüssel, Belgien
    "ATH",  # Athen, Griechenland
    "PRG",  # Prag, Tschechien
    "LIS",  # Lissabon, Portugal
    "BUD",  # Budapest, Ungarn
    "BEG",  # Belgrad, Serbien
    "VIE",  # Wien, Österreich
    "ZRH",  # Bern/Zürich, Schweiz
    "SOF",  # Sofia, Bulgarien
    "CPH",  # Kopenhagen, Dänemark
    "HEL",  # Helsinki, Finnland
    "OSL",  # Oslo, Norwegen
    "DUB",  # Dublin, Irland
]



options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Optional zur Vermeidung von Bot-Erkennung
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

try:
    for city in iata_codes:
        url = f"https://www.momondo.at/explore/{city}-anywhere"
        driver.get(url)
        time.sleep(random.uniform(50, 60))

        dateiname = f"Project/Html/momondoHTML/momondo_{city}_{heute.strftime('%m%d')}.html"
        with open(dateiname, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print(f"Seite wurde gespeichert als {dateiname}")

finally:
    driver.quit()
    print("Fertig")

