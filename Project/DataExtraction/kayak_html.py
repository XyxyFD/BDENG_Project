from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Pfad zum Ordner mit HTML-Dateien
html_folder = "Project/Html/kayakHTML"

# Liste, um alle extrahierten Daten zu sammeln
all_angebote = []

# Durchsuche alle HTML-Dateien im Ordner
for filename in os.listdir(html_folder):
    if filename.endswith(".html") and filename.startswith("kayak_"):
        file_path = os.path.join(html_folder, filename)
        
        # Dateinamen parsen, um Abflug-Flughafen und Datum zu extrahieren
        match = re.search(r"kayak_([A-Z]{3})_(\d{2})(\d{2})\.html", filename)
        airport_code = match.group(1) if match else "N/A"
        day = match.group(2) if match else "N/A"
        month = match.group(3) if match else "N/A"
        
        # HTML-Datei laden
        with open(file_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Alle Einträge mit der Klasse "Blek-wrapper"
        blocks = soup.select("div.Blek-wrapper")

        for block in blocks:
            city_tag = block.select_one("div.LGqM")
            price_tag = block.select_one("div.Blek-title")

            if city_tag and price_tag:
                city = city_tag.get_text(strip=True)
                # Nur Zahl aus Preis extrahieren
                match_price = re.search(r"\d+", price_tag.get_text())
                price = int(match_price.group()) if match_price else None

                all_angebote.append({
                    "Abflug_Flughafen": airport_code,
                    "Datum": f"{day}.{month}",
                    "Stadt": city,
                    "Preis": price
                })

# CSV speichern
df = pd.DataFrame(all_angebote)
df.to_csv("Project/csv/kayak_data.csv", index=False, encoding="utf-8")

print("Fertig – Daten aus allen HTML-Dateien im kayakHTML-Ordner gesammelt und in kayak_data.csv gespeichert.")
