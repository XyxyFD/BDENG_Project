import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Pfade zu den CSV-Dateien
INPUT_CSV = 'Project/SEO_Analysis/unique_search_terms.csv'                 # CSV mit einer Spalte: jeder Suchterm in einer eigenen Zeile
OUTPUT_CSV = 'Project/SEO_Analysis/search_results_duckduckgo_USA.csv'          # Ausgabe-CSV: search_term, link1 ... link10

# 1. Alle Suchbegriffe aus der Eingabe-CSV einlesen
suchbegriffe = []
with open(INPUT_CSV, newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if row and row[0].strip():
            # Falls eine Kopfzeile existiert, ignorieren
            if row[0].strip().lower() == 'search_term':
                continue
            suchbegriffe.append(row[0].strip())

# 2. Ausgabe-CSV vorbereiten und Kopfzeile schreiben
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow([
        'search_term',
        'link1', 'link2', 'link3', 'link4', 'link5',
        'link6', 'link7', 'link8', 'link9', 'link10'
    ])

    # 3. Selenium WebDriver (Chrome) starten
    options = webdriver.ChromeOptions()
    # Headless auskommentiert, um CAPTCHAs zu reduzieren
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    for term in suchbegriffe:
        try:
            # a) DuckDuckGo öffnen
            driver.get('https://duckduckgo.com/')
            time.sleep(random.uniform(1, 2))

            # b) Suchfeld finden, Begriff eingeben und Suche starten
            suchfeld = driver.find_element(By.NAME, 'q')
            suchfeld.clear()
            suchfeld.send_keys(term)
            suchfeld.send_keys(Keys.RETURN)

            # c) Wartezeit (2–4 Sekunden), bis Ergebnisse erscheinen
            time.sleep(random.uniform(2, 4))

            # d) Die ersten 10 <p>-Tags mit genau dieser Klasse auswählen
            links = []
            css_class = "veU5I0hFkgFGOPhX2RBE wZ4JdaHxSAhGy1HoNVja AlPVsxUsFt3bnuOvg6hI"
            selector = "p." + ".".join(css_class.split())
            ergebnisse = driver.find_elements(By.CSS_SELECTOR, selector)[:10]

            for p_tag in ergebnisse:
                # Erstes <span> innerhalb von <p> auslesen
                span1 = p_tag.find_element(By.TAG_NAME, 'span')
                text = span1.text.strip()
                # "https://" bzw. "http://" entfernen, falls vorhanden
                if text.startswith("https://"):
                    text = text.replace("https://", "", 1)
                elif text.startswith("http://"):
                    text = text.replace("http://", "", 1)
                links.append(text)

            # e) Falls weniger als 10 gefunden wurden, mit leeren Strings auffüllen
            while len(links) < 10:
                links.append('')

            # f) Zeile in die Ausgabe-CSV schreiben
            writer.writerow([term] + links)

            # g) Kurze Pause, bevor zum nächsten Begriff gewechselt wird
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            # Bei Fehler: trotzdem eine Zeile mit leeren Links schreiben und Fehler protokollieren
            writer.writerow([term] + [''] * 10)
            print(f"Fehler bei DuckDuckGo-Suche '{term}': {e}")

    # 4. Browser schließen
    driver.quit()
