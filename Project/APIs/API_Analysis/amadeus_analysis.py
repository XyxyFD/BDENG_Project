import pandas as pd
import matplotlib.pyplot as plt
import os

filepath_amadeus_BER = "../PricesCSV/amadeus_prices_BER.csv"
filepath_amadeus_CDG = "../PricesCSV/amadeus_prices_CDG.csv"
filepath_amadeus_IST = "../PricesCSV/amadeus_prices_IST.csv"
filepath_amadeus_LHR = "../PricesCSV/amadeus_prices_LHR.csv"

amadeus_BER = pd.read_csv(filepath_amadeus_BER)
amadeus_CDG = pd.read_csv(filepath_amadeus_CDG)
amadeus_IST = pd.read_csv(filepath_amadeus_IST)
amadeus_LHR = pd.read_csv(filepath_amadeus_LHR)

# Stelle sicher, dass FetchedAt als datetime erkannt wird
amadeus_BER['FetchedAt'] = pd.to_datetime(amadeus_BER['FetchedAt'])

# Nur Datum + Stunde + Minute behalten
amadeus_BER['FetchedAt'] = amadeus_BER['FetchedAt'].dt.strftime('%Y-%m-%d %H:%M')

# einziger gemeinsamer Zielflughafen ist FCO Für Rome Fiumicino "Leonardo da Vinci" Airport

abflughäfen = ['BER', 'CDG', 'IST', 'LHR']

for airport in abflughäfen:
    df = globals()[f'amadeus_{airport}']
    meanpreis = df[df['Destination'] == 'FCO']['MinPrice'].mean()
    print(f"Durchschnittspreis {airport} → FCO: {meanpreis:.2f} €")

# --------------------------------------------------------------------------------------------
# Plots erstellen
durchschnittspreise = []
# Neue Liste für DataFrame
rows = []

for airport in abflughäfen:
    df = globals()[f'amadeus_{airport}']
    vorher = df.shape[0]
    df.dropna(inplace=True)
    nachher = df.shape[0]
    print(f"{airport}: {vorher - nachher} Zeile(n) mit fehlenden Werten entfernt.")
    meanpreis = df[df['Destination'] == 'FCO']['MinPrice'].mean()
    durchschnittspreise.append(meanpreis)
    rows.append({'Quelle': 'Amadeus', 'Abflug': airport, 'Durchschnittspreis': meanpreis})

# Exportiere CSV-Datei
os.makedirs("mean_prices_to_FCO", exist_ok=True)
df_amadeus_export = pd.DataFrame(rows)
df_amadeus_export.to_csv("mean_prices_to_FCO/amadeus_durchschnittspreise_fco.csv", index=False)
print("Datei erfolgreich gespeichert:", os.path.exists("mean_prices_to_FCO/amadeus_durchschnittspreise_fco.csv"))


# Balkendiagramm
plt.figure(figsize=(8, 5))
bars = plt.bar(abflughäfen, durchschnittspreise, color='skyblue')
plt.ylabel("Durchschnittspreis (€)")
plt.title("Durchschnittspreise nach FCO – Amadeus")

# Werte über den Balken anzeigen
for bar, preis in zip(bars, durchschnittspreise):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{preis:.0f} €",
             ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()