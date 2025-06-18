import pandas as pd

# --------------- Konfiguration ----------------
INPUT_CSV = 'Project/SEO_Analysis/flights_tickets_serp2019-06-01.csv'
REDUCED_CSV = 'Project/SEO_Analysis/serp_reduced.csv'          # enthält nur searchTerms, rank, displayLink
UNIQUE_TERMS_CSV = 'Project/SEO_Analysis/unique_search_terms.csv'  # je ein Suchbegriff pro Zeile
# -----------------------------------------------

def main():
    # 1. Original-CSV einlesen
    df = pd.read_csv(INPUT_CSV, encoding='utf-8')

    # 2. Nur die drei Spalten auswählen: searchTerms, rank, displayLink
    df_reduced = df.loc[:, ['searchTerms', 'rank', 'displayLink']]

    # 3. Aufbereiten: CSV ohne Index speichern
    df_reduced.to_csv(REDUCED_CSV, index=False, encoding='utf-8')

    # 4. Einzigartige Suchbegriffe extrahieren
    unique_terms = df_reduced['searchTerms'].drop_duplicates().reset_index(drop=True)

    # 5. In eine neue CSV schreiben (mit Kopfzeile "search_term")
    unique_terms_df = pd.DataFrame({'search_term': unique_terms})
    unique_terms_df.to_csv(UNIQUE_TERMS_CSV, index=False, header=True, encoding='utf-8')

    print(f"→ '{REDUCED_CSV}' angelegt (Spalten: searchTerms, rank, displayLink)")
    print(f"→ '{UNIQUE_TERMS_CSV}' angelegt (einzigartige Suchbegriffe)")

if __name__ == '__main__':
    main()
