import pandas as pd

# ======== KONFIGURACJA NAZW PLIKÓW ========
EMP_FILE = 'empik.xlsx'
ALLE_FILE = 'allegro.xlsx'
OUT_FILE = 'wynik.xlsx'
# ==========================================

def main():
    print("\n✅ Kolumna A → zawsze ID")
    print("✅ Kolumna B → zawsze Cena")
    print("✅ Kolumna C → zawsze Ilość")
    print("ℹ️ Nie ma znaczenia co masz w nagłówku w Excelu – kod ustawia to na sztywno.\n")

    # 1️⃣ Wczytaj pliki Excel i wymuś nagłówki
    empik_df = pd.read_excel(EMP_FILE, header=None, names=['ID', 'Cena', 'Ilość'])
    allegro_df = pd.read_excel(ALLE_FILE, header=None, names=['ID', 'Cena', 'Ilość'])

    print("✅ EMPIK:")
    print(empik_df.head(), '\n')

    print("✅ ALLEGRO:")
    print(allegro_df.head(), '\n')

    # 2️⃣ Połącz dane (LEFT JOIN – wszystkie ID z Empik)
    result = pd.merge(
        empik_df[['ID']],
        allegro_df,
        on='ID',
        how='left'
    )

    # 3️⃣ Uzupełnij brakujące wartości zerami
    result['Cena'] = result['Cena'].fillna(0)
    result['Ilość'] = result['Ilość'].fillna(0).astype(int)

    print("✅ Wynik końcowy:")
    print(result.head())

    # 4️⃣ Zapisz do Excel
    result.to_excel(OUT_FILE, index=False)
    print(f"\n✅ Wynik zapisany do pliku: {OUT_FILE}")

if __name__ == '__main__':
    main()
