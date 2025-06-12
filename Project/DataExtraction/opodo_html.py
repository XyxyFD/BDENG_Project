from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Pfad zum Ordner mit HTML-Dateien
html_folder = "Project/Html/opodoHTML"

# Liste, um alle extrahierten Daten zu sammeln
all_angebote = []

# Durchsuche alle HTML-Dateien im Ordner
for filename in os.listdir(html_folder):
    if filename.endswith(".html") and filename.startswith("opodo_"):
        file_path = os.path.join(html_folder, filename)
        
        # Dateinamen parsen, um Domain, Datum und Uhrzeit zu extrahieren
        match = re.search(r"opodo_([a-z]{2})_(\d{2})(\d{2})_(\d{2})(\d{2})\.html", filename)
        
        domain_abbr = match.group(1) if match else "N/A"
        day = match.group(3) if match else "N/A"
        month = match.group(2) if match else "N/A"
        hour = match.group(4) if match else "N/A"
        minute = match.group(5) if match else "N/A"
        
        # HTML-Datei laden
        with open(file_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Ergebnisse sammeln
        # angebote = [] # This line is no longer needed here

        # 1) Container auswählen
        containers = soup.select("div.css-1upemms.e17fzqxg0")

        # angebote = [] # This line is no longer needed here
        for box in containers:
            city_tag  = box.select_one("div.css-1n4nh93.e1hue9ey0")
            price_tag = box.select_one("span.css-1p8lfkf")

            price_tag = box.select_one("span.money-integer.css-1p8lfkf.e139ay0z2")

            if(city_tag == None):
                city_tag = box.select_one("div.css-1qkt9ba.e1hue9ey0")

            if city_tag and price_tag:
                city  = city_tag.get_text(strip=True)
                match_price = re.search(r"\d+", price_tag.get_text())
                price = int(match_price.group()) if match_price else None
                
                all_angebote.append({
                    "Domain": domain_abbr,
                    "Datum": f"{day}.{month}",
                    "Uhrzeit": f"{hour}:{minute}",
                    "Stadt": city,
                    "Preis": price
                })


# CSV speichern
df = pd.DataFrame(all_angebote)
df.to_csv("Project/csv/opodo_data.csv", index=False, encoding="utf-8")

print("Fertig – Daten aus allen HTML-Dateien im opodoHTML-Ordner gesammelt und in opodo_data.csv gespeichert.")
