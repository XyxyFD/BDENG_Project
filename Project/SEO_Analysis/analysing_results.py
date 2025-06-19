import pandas as pd
import matplotlib.pyplot as plt

# Datei-Pfade
file_serp = "Project/SEO_Analysis/serp_reduced.csv"
file_duck = "Project/SEO_Analysis/search_results_duckduckgo.csv"
file_duck_USA = "Project/SEO_Analysis/search_results_duckduckgo_USA.csv"

# CSVs laden
df_serp = pd.read_csv(file_serp)
df_duck = pd.read_csv(file_duck)
df_duck_USA = pd.read_csv(file_duck_USA)

# SERP vereinheitlichen
df_serp = df_serp.rename(columns={'searchTerms': 'search_term', 'displayLink': 'domain'})
df_serp['source'] = 'SERP'

# DuckDuckGo ins Long-Format
def melt_duckduckgo(df, source_name):
    records = []
    for _, row in df.iterrows():
        term = row['search_term']
        for i in range(1, 11):
            records.append({
                'search_term': term,
                'rank': i,
                'domain': row[f'link{i}'],
                'source': source_name
            })
    return pd.DataFrame(records)

df_duck_long = melt_duckduckgo(df_duck, 'DuckDuckGo')
df_duck_USA_long = melt_duckduckgo(df_duck_USA, 'DuckDuckGo_USA')

# Scores berechnen (Platz 1 = 10 Punkte)
df_serp['score'] = 11 - df_serp['rank']
df_duck_long['score'] = 11 - df_duck_long['rank']
df_duck_USA_long['score'] = 11 - df_duck_USA_long['rank']

# Stats pro Domain
def get_stats(df):
    return df.groupby('domain').agg(
        appearances=('domain', 'count'),
        avg_rank=('rank', 'mean'),
        total_score=('score', 'sum')
    ).sort_values(by='total_score', ascending=False).reset_index()

# Auswertungen
stats_serp = get_stats(df_serp).head(15)
stats_duck = get_stats(df_duck_long).head(15)
stats_duck_USA = get_stats(df_duck_USA_long).head(15)

# Plot 1: SERP
plt.figure(figsize=(10, 6))
plt.barh(stats_serp['domain'], stats_serp['total_score'], color='orange')
plt.xlabel("Gesamtscore (gewichtete Sichtbarkeit)")
plt.title("Top 15 Domains – SERP 2019")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Plot 2: DuckDuckGo
plt.figure(figsize=(10, 6))
plt.barh(stats_duck['domain'], stats_duck['total_score'], color='skyblue')
plt.xlabel("Gesamtscore (gewichtete Sichtbarkeit)")
plt.title("Top 15 Domains – DuckDuckGo 2025")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Plot 3: DuckDuckGo USA
plt.figure(figsize=(10, 6))
plt.barh(stats_duck_USA['domain'], stats_duck_USA['total_score'], color='lightgreen')
plt.xlabel("Gesamtscore (gewichtete Sichtbarkeit)")
plt.title("Top 15 Domains – DuckDuckGo USA 2025")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Optional: Ausgabe der Tabellen
print("\nTop 15 Domains – SERP 2019:")
print(stats_serp.to_string(index=False))

print("\nTop 15 Domains – DuckDuckGo 2025:")
print(stats_duck.to_string(index=False))

print("\nTop 15 Domains – DuckDuckGo USA 2025:")
print(stats_duck_USA.to_string(index=False))
