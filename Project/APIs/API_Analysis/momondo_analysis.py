import pandas as pd
import matplotlib.pyplot as plt
import os

filepath_momondo = "../../csv/momondo_data.csv"

momondo_df = pd.read_csv(filepath_momondo)

# Liste der gewünschten Flughäfen
ziel_airports = ['BER', 'CDG', 'IST', 'LHR']

# Für jeden dieser Flughäfen ein DataFrame als eigene Variable erstellen
for airport in ziel_airports:
    globals()[f"momondo_{airport}"] = momondo_df[momondo_df['Abflug_Flughafen'] == airport].copy()

for airport in ['BER', 'CDG', 'IST', 'LHR']:
    df = globals()[f'momondo_{airport}']
    df = df.rename(columns={'Stadt': 'Zielflughafen'})
    df['Zielflughafen'] = df['Zielflughafen'].apply(
        lambda x: x.split('(')[-1].replace(')', '').strip() if '(' in x else x.strip()
    )
    globals()[f'momondo_{airport}'] = df

# Durchschnittspreis der Flüge nach FCO (Rom, Italien) berechnen
for airport in ziel_airports:
    df = globals()[f'momondo_{airport}']
    meanpreis = df[df['Zielflughafen'] == 'FCO']['Preis'].mean()
    print(f"Durchschnittspreis {airport} → FCO: {meanpreis:.2f} €")

# --------------------------------------------------------------------------------------------
# Plots erstellen
durchschnittspreise = []
# Neue Liste für DataFrame
rows = []

for airport in ziel_airports:
    df = globals()[f'momondo_{airport}']
    vorher = df.shape[0]
    df.dropna(inplace=True)
    nachher = df.shape[0]
    print(f"{airport}: {vorher - nachher} Zeile(n) mit fehlenden Werten entfernt.")
    meanpreis = df[df['Zielflughafen'] == 'FCO']['Preis'].mean()
    durchschnittspreise.append(meanpreis)
    rows.append({'Quelle': 'Momondo', 'Abflug': airport, 'Durchschnittspreis': meanpreis})

# Exportiere CSV-Datei
os.makedirs("mean_prices_to_FCO", exist_ok=True)
df_momondo_export = pd.DataFrame(rows)
df_momondo_export.to_csv("mean_prices_to_FCO/momondo_durchschnittspreise_fco.csv", index=False)
print("Datei erfolgreich gespeichert:", os.path.exists("mean_prices_to_FCO/momondo_durchschnittspreise_fco.csv"))

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