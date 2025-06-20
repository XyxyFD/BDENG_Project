import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSVs laden
df_kayak = pd.read_csv("mean_prices_to_FCO/kayak_durchschnittspreise_fco.csv")
df_momondo = pd.read_csv("mean_prices_to_FCO/momondo_durchschnittspreise_fco.csv")
df_amadeus = pd.read_csv("mean_prices_to_FCO/amadeus_durchschnittspreise_fco.csv")

# Zusammenführen in einen einzigen DataFrame
df_gesamt = pd.concat([df_kayak, df_momondo, df_amadeus], ignore_index=True)

# Pivot-Tabelle: Abflug in Zeilen, Quelle in Spalten
df_pivot = df_gesamt.pivot(index='Abflug', columns='Quelle', values='Durchschnittspreis')

# Plot vorbereiten
x = np.arange(len(df_pivot.index))  # Positionen der Abflughäfen
width = 0.25  # Breite pro Balkengruppe

# Plot
plt.figure(figsize=(10, 6))
bars_k = plt.bar(x - width, df_pivot['Kayak'], width=width, label='Kayak', color='coral')
bars_m = plt.bar(x, df_pivot['Momondo'], width=width, label='Momondo', color='skyblue')
bars_a = plt.bar(x + width, df_pivot['Amadeus'], width=width, label='Amadeus API', color='lightgreen')

# Beschriftung über den Balken
for bars in [bars_k, bars_m, bars_a]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.2f} €",
                 ha='center', va='bottom', fontsize=9)

# Achsenbeschriftungen
plt.xlabel("Abflughafen")
plt.ylabel("Durchschnittspreis (€)")
plt.title("Vergleich der Durchschnittspreise nach FCO")
plt.xticks(x, df_pivot.index)
plt.legend()
plt.tight_layout()
plt.savefig("Pictures/durchschnittspreise_fco_vergleich.png", dpi=300)
plt.show()
