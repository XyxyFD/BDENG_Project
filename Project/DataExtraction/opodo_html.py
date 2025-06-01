from bs4 import BeautifulSoup
import pandas as pd
import re

# HTML-Datei laden
with open("opodo_0527_2122.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Ergebnisse sammeln
angebote = []

# 1) Container auswählen
containers = soup.select("div.css-1upemms.e17fzqxg0")

angebote = []
for box in containers:
    city_tag  = box.select_one("div.css-1n4nh93.e1hue9ey0")
    price_tag = box.select_one("span.css-1p8lfkf")

    price_tag = box.select_one("span.money-integer.css-1p8lfkf.e139ay0z2")

    if(city_tag == None):
        city_tag = box.select_one("div.css-1qkt9ba.e1hue9ey0")

    if city_tag and price_tag:
        city  = city_tag.get_text(strip=True)
        price = int(re.search(r"\d+", price_tag.get_text()).group())
        angebote.append({"Stadt": city, "Preis": price})


# CSV speichern
df = pd.DataFrame(angebote)
df.to_csv("opodo.csv", index=False, encoding="utf-8")

print("Fertig – Daten in opodo.csv gespeichert.")


'''

import os
from bs4 import BeautifulSoup
import pandas as pd
import re

# Ordnerpfad anpassen
folder = "../Html/opodoHTML"
alle_angebote = []

for filename in os.listdir(folder):
    if filename.endswith(".html"):
        filepath = os.path.join(folder, filename)
        with open(filepath, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        containers = soup.select("div.css-1upemms.e17fzqxg0")
        for box in containers:
            city_tag  = box.select_one("div.css-1n4nh93.e1hue9ey0")
            price_tag = box.select_one("span.css-1p8lfkf")
            price_tag = box.select_one("span.money-integer.css-1p8lfkf.e139ay0z2")
            if city_tag is None:
                city_tag = box.select_one("div.css-1qkt9ba.e1hue9ey0")
            if city_tag and price_tag:
                city  = city_tag.get_text(strip=True)
                price = int(re.search(r"\d+", price_tag.get_text()).group())
                alle_angebote.append({"Datei": filename, "Stadt": city, "Preis": price})

# CSV speichern
df = pd.DataFrame(alle_angebote)
df.to_csv("opodo_alle.csv", index=False, encoding="utf-8")
print("Fertig – Daten aus allen HTML-Dateien gespeichert.")

'''