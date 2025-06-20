import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

filepath_opodo = "../../csv/opodo_data.csv"

opodo_df = pd.read_csv(filepath_opodo)

vorher = opodo_df.shape[0]
opodo_df.dropna(inplace=True)
nachher = opodo_df.shape[0]
print(f"{vorher - nachher} Zeile(n) mit fehlenden Werten entfernt.")

# Einzigartige Städte aus der Spalte 'Stadt'
alle_staedte = opodo_df['Stadt'].dropna().unique()

stadt_aliases = {
    'París': 'Paris',
    'Parigi': 'Paris',
    'Londres': 'London',
    'Londra': 'London',
    'Londen': 'London',
    'Barcelone': 'Barcelona',
    'Barcellona': 'Barcelona',
    'Milán': 'Milan',
    'Milano': 'Milan',
    'Milaan': 'Milan',
    'Milán': 'Milan',
    'Milão': 'Milan',
    'Estambul': 'Istanbul',
    'Wenen': 'Wien',
    'Lisbonne': 'Lissabon',
    'Amsterdã': 'Amsterdam',
    'Ámsterdam': 'Amsterdam',
    'Venetië': 'Venedig',
    'Praag': 'Prag',
    'Praga': 'Prag',
    'Roma': 'Rom',
    'Valenza': 'Valencia',
    'Valência': 'Valencia',
    'Bruxelas': 'Brüssel',
    'Bruselas': 'Brüssel',
    'Ginebra': 'Genf',
    'Luxemburgo': 'Luxemburg',
}

stadt_to_iata = {
    'Paris': 'CDG',
    'London': 'LHR',
    'Rome': 'FCO',
    'Rom': 'FCO',
    'Barcelona': 'BCN',
    'Istanbul': 'IST',
    'Madrid': 'MAD',
    'Milan': 'MXP',
    'Amsterdam': 'AMS',
    'Berlin': 'BER',
    'Hamburg': 'HAM',
    'Belgrad': 'BEG',
    'Köln': 'CGN',
    'Zürich': 'ZRH',
    'Antalya': 'AYT',
    'Wien': 'VIE',
    'Ibiza': 'IBZ',
    'Brüssel': 'BRU',
    'Genf': 'GVA',
    'Lanzarote': 'ACE',
    'Bucarest': 'OTP',
    'Venedig': 'VCE',
    'Tirana': 'TIA',
    'Tenerife': 'TFS',
    'Alger': 'ALG',
    'Tunis': 'TUN',
    'Lissabon': 'LIS',
    'Porto': 'OPO',
    'Marrakech': 'RAK',
    'Casablanca': 'CMN',
    'Faro': 'FAO',
    'Catania': 'CTA',
    'Palermo': 'PMO',
    'Valencia': 'VLC',
    'Olbia': 'OLB',
    'Alicante': 'ALC',
    'Dublin': 'DUB',
    'Nice': 'NCE',
    'Malta': 'MLA',
    'Prag': 'PRG',
    'Luxemburg': 'LUX',
    'Funchal': 'FNC',
    'Ponta': 'PDL',
    'Terceira': 'TER'
}

# Zuordnung: Domain → Abflughafen
domain_to_abflug = {
    'at': 'VIE',
    'de': 'BER',
    'es': 'MAD',
    'fr': 'CDG',
    'it': 'FCO',
    'nl': 'AMS',
    'pt': 'LIS'
}

# Schritt 1: Vereinheitlichung
opodo_df['Zielflughafen'] = opodo_df['Stadt'].apply(lambda x: stadt_aliases.get(x, x))

# Schritt 2: IATA-Zuweisung
opodo_df['Zielflughafen'] = opodo_df['Zielflughafen'].map(stadt_to_iata)

# Eindeutige Domain-Werte extrahieren
unique_domains = opodo_df['Domain'].unique()

# Für jede Domain einen eigenen DataFrame als Variable erzeugen
for domain in unique_domains:
    globals()[f"opodo_{domain}"] = opodo_df[opodo_df['Domain'] == domain].copy()

# Zielflughäfen = alle anderen Abflugorte
alle_abfluege = list(domain_to_abflug.values())

# Liste für Ergebnisse
rows = []

# Berechne von jedem Startflughafen zu allen anderen
for domain, abflug in domain_to_abflug.items():
    df = globals()[f'opodo_{domain}']  # Hole den passenden DataFrame

    for ziel in alle_abfluege:
        if abflug == ziel:
            continue  # Kein Flug zu sich selbst

        preis = round(df[df['Zielflughafen'] == ziel]['Preis'].mean(), 2)
        rows.append({
            'Abflug': abflug,
            'Ziel': ziel,
            'Durchschnittspreis': preis
        })

# In DataFrame umwandeln
preis_matrix = pd.DataFrame(rows)

# Ergebnis anzeigen
print(preis_matrix)

# Pivotieren für Heatmap: Zeilen = Abflug, Spalten = Ziel
preis_pivot = preis_matrix.pivot(index='Abflug', columns='Ziel', values='Durchschnittspreis')

# Plot
plt.figure(figsize=(10, 6))
sns.heatmap(preis_pivot, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5)
plt.title("Durchschnittspreise zwischen europäischen Hauptstädten (Opodo)")
plt.xlabel("Zielflughafen")
plt.ylabel("Abflugflughafen")
plt.tight_layout()
plt.savefig("Pictures/durchschnittspreise_hauptstaedte_vergleich_opodo.png", dpi=300)
plt.show()

# Plot 2
plt.figure(figsize=(10, 6))
sns.boxplot(data=opodo_df, x='Domain', y='Preis', palette='Set2')
plt.title("Preisverteilung je Domain (Opodo)")
plt.xlabel("Domain")
plt.ylabel("Flugpreis (€)")
plt.tight_layout()
plt.savefig("Pictures/preisverteilung_je_domain_opodo.png", dpi=300)
plt.show()