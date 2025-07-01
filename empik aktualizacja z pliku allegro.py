import pandas as pd

# ======== KONFIGURACJA ========
EMP_FILE = 'empik.xlsx'         # plik Empik
ALLE_FILE = 'allegro.xlsx'      # plik Allegro
OUT_FILE = 'wynik.xlsx'         # plik wynikowy
# ==============================

def main():
    print("\nℹ️ Upewnij się, że pliki Excel mają nagłówki w pierwszym wierszu:")
    print("Kolumna A = ID, Kolumna B = Cena, Kolumna C = Ilość")
    print("Przykład nagłówka: ID | Cena | Ilość\n")

    # 1️⃣ Wczytanie plików Excel z nagłówkiem
    empik_df = pd.read_excel(EMP_FILE)
    allegro_df = pd.read_excel(ALLE_FILE)

    print("✅ Wczytano plik Empik:")
    print(empik_df.head(), '\n')
    
    print("✅ Wczytano plik Allegro:")
    print(allegro_df.head(), '\n')

    # 2️⃣ LEFT JOIN – zachowujemy WSZYSTKIE ID z Empik
    merged = pd.merge(
        empik_df[['ID']],        # tylko kolumna ID z Empik
        allegro_df,              # pełne dane z Allegro
        on='ID',
        how='left'
    )

    # 3️⃣ Wypełnienie braków zerami
    merged['Cena'] = merged['Cena'].fillna(0)
    merged['Ilość'] = merged['Ilość'].fillna(0).astype(int)

    print("✅ Wynik po połączeniu:")
    print(merged.head(), '\n')

    # 4️⃣ Zapis do pliku Excel
    merged.to_excel(OUT_FILE, index=False)
    print(f"✅ Wynik zapisany do pliku: {OUT_FILE}")

if __name__ == '__main__':
    main()
