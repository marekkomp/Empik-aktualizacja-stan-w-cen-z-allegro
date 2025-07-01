import pandas as pd

# ======== KONFIGURACJA NAZW PLIKÓW ========
EMP_FILE = 'empik.xlsx'
ALLE_FILE = 'allegro.xlsx'
OUT_FILE = 'wynik.xlsx'
# ==========================================

def clean_id_column(series):
    """
    Funkcja czyszcząca kolumnę ID:
    - konwertuje wszystko na tekst
    - usuwa spacje
    - zamienia na wielkie litery
    """
    return (
        series
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r'[^A-Z0-9]', '', regex=True)  # opcjonalne: usunie znaki specjalne
    )

def main():
    print("\n✅ Kolumna A → zawsze ID")
    print("✅ Kolumna B → zawsze Cena")
    print("✅ Kolumna C → zawsze Ilość")
    print("ℹ️ Nagłówki z pliku są ignorowane – kod ustawia je na sztywno.")
    print("ℹ️ ID są czyszczone i normalizowane (spacje, wielkie litery).\n")

    # 1️⃣ Wczytaj pliki Excel i wymuś nagłówki
    empik_df = pd.read_excel(EMP_FILE, header=None, names=['ID', 'Cena', 'Ilość'])
    allegro_df = pd.read_excel(ALLE_FILE, header=None, names=['ID', 'Cena', 'Ilość'])

    print("✅ Wczytano EMPIK:")
    print(empik_df.head(), '\n')

    print("✅ Wczytano ALLEGRO:")
    print(allegro_df.head(), '\n')

    # 2️⃣ Czyszczenie i normalizacja kolumny ID
    empik_df['ID'] = clean_id_column(empik_df['ID'])
    allegro_df['ID'] = clean_id_column(allegro_df['ID'])

    print("✅ Po czyszczeniu kolumny ID:")
    print("EMPIK IDs:", empik_df['ID'].unique())
    print("ALLEGRO IDs:", allegro_df['ID'].unique(), '\n')

    # 3️⃣ Połącz dane (LEFT JOIN – wszystkie ID z Empik)
    result = pd.merge(
        empik_df[['ID']],
        allegro_df,
        on='ID',
        how='left'
    )

    # 4️⃣ Uzupełnij brakujące wartości zerami
    result['Cena'] = result['Cena'].fillna(0)
    result['Ilość'] = result['Ilość'].fillna(0).astype(int)

    print("✅ Wynik końcowy:")
    print(result.head())

    # 5️⃣ Zapisz do Excel
    result.to_excel(OUT_FILE, index=False)
    print(f"\n✅ Wynik zapisany do pliku: {OUT_FILE}")

if __name__ == '__main__':
    main()
