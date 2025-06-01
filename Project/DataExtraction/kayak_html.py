from bs4 import BeautifulSoup
import pandas as pd
import re

# HTML-Datei laden
with open("kayak_0525.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Ergebnisse sammeln
angebote = []

# Alle Einträge mit der Klasse "Blek-wrapper"
blocks = soup.select("div.Blek-wrapper")

for block in blocks:
    city_tag = block.select_one("div.LGqM")
    price_tag = block.select_one("div.Blek-title")

    if city_tag and price_tag:
        city = city_tag.get_text(strip=True)
        # Nur Zahl aus Preis extrahieren
        match = re.search(r"\d+", price_tag.get_text())
        price = int(match.group()) if match else None

        angebote.append({"Stadt": city, "Preis": price})

# CSV speichern
df = pd.DataFrame(angebote)
df.to_csv("kayak_0525.csv", index=False, encoding="utf-8")

print("Fertig – Daten aus .Blek-Blöcken gespeichert.")
