import pandas as pd
import matplotlib.pyplot as plt
import os

filepath_kayak = "../../csv/kayak_data.csv"

kayak_df = pd.read_csv(filepath_kayak)

# Liste der gewünschten Flughäfen
ziel_airports = ['BER', 'CDG', 'IST', 'LHR']

# Für jeden dieser Flughäfen ein DataFrame als eigene Variable erstellen
for airport in ziel_airports:
    globals()[f"kayak_{airport}"] = kayak_df[kayak_df['Abflug_Flughafen'] == airport].copy()

# Spalte Stadt in Zielflughafen umbenennen und nur den IATA Code speichern
for airport in ['BER', 'CDG', 'IST', 'LHR']:
    df = globals()[f'kayak_{airport}']
    df = df.rename(columns={'Stadt': 'Zielflughafen'})
    df['Zielflughafen'] = df['Zielflughafen'].apply(
        lambda x: x.split('(')[-1].replace(')', '').strip() if '(' in x else x.strip()
    )
    globals()[f'kayak_{airport}'] = df

# Für jeden Flughafen: Zielflughäfen zählen und anzeigen
#for airport in ziel_airports:
#    df = globals()[f'kayak_{airport}']
#    ziel_counts = df['Zielflughafen'].value_counts().reset_index()
#    ziel_counts.columns = ['Zielflughafen', 'Anzahl']
#    print(f"\nZielflughäfen ab {airport}:\n", ziel_counts)


# Für jeden DataFrame prüfen, wie viele Flüge nach FCO gehen
#for airport in ziel_airports:
#    df = globals()[f'kayak_{airport}']
#    anzahl_fco = df[df['Zielflughafen'] == 'FCO'].shape[0]
#    print(f"Anzahl Flüge von {airport} nach FCO: {anzahl_fco}")

# Durchschnittspreis der Flüge nach FCO (Rom, Italien) berechnen
for airport in ziel_airports:
    df = globals()[f'kayak_{airport}']
    meanpreis = df[df['Zielflughafen'] == 'FCO']['Preis'].mean()
    print(f"Durchschnittspreis {airport} → FCO: {meanpreis:.2f} €")

# --------------------------------------------------------------------------------------------
# Plots erstellen
durchschnittspreise = []
# Neue Liste für DataFrame
rows = []

for airport in ziel_airports:
    df = globals()[f'kayak_{airport}']
    vorher = df.shape[0]
    df.dropna(inplace=True)
    nachher = df.shape[0]
    print(f"{airport}: {vorher - nachher} Zeile(n) mit fehlenden Werten entfernt.")
    meanpreis = df[df['Zielflughafen'] == 'FCO']['Preis'].mean()
    durchschnittspreise.append(meanpreis)
    rows.append({'Quelle': 'Kayak', 'Abflug': airport, 'Durchschnittspreis': meanpreis})

# Exportiere CSV-Datei
os.makedirs("mean_prices_to_FCO", exist_ok=True)
df_kayak_export = pd.DataFrame(rows)
df_kayak_export.to_csv("mean_prices_to_FCO/kayak_durchschnittspreise_fco.csv", index=False)
print("Datei erfolgreich gespeichert:", os.path.exists("mean_prices_to_FCO/kayak_durchschnittspreise_fco.csv"))

# Balkendiagramm zeichnen
plt.figure(figsize=(8, 5))
bars = plt.bar(ziel_airports, durchschnittspreise, color='coral')
plt.ylabel("Durchschnittspreis (€)")
plt.title("Durchschnittspreise nach FCO – Kayak")

for bar, preis in zip(bars, durchschnittspreise):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{preis:.2f} €",
             ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()