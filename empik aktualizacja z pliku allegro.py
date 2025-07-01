import streamlit as st
import pandas as pd

st.title("Empik – aktualizacja stanu i ceny z pliku Allegro")

st.info("""
ℹ️ Ta aplikacja zawsze wymusza układ kolumn:
- Kolumna A → ID  
- Kolumna B → Cena  
- Kolumna C → Ilość  
Nagłówki z Twoich plików są IGNOROWANE!
""")

# uploader
empik_file   = st.file_uploader("📤 Wgraj plik EMPiK (.xlsx)",   type=["xlsx"])
allegro_file = st.file_uploader("📤 Wgraj plik ALLEGRO (.xlsx)", type=["xlsx"])

def clean_id_column(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
         .str.strip()
         .str.upper()
         .str.replace(r'[^A-Z0-9]', '', regex=True)
    )

if empik_file and allegro_file:
    try:
        # 1️⃣ Wczytujemy z uploaderów i narzucamy nazwy kolumn
        empik_df   = pd.read_excel(empik_file,   header=None, names=['ID','Cena','Ilość'])
        allegro_df = pd.read_excel(allegro_file, header=None, names=['ID','Cena','Ilość'])

        # 2️⃣ Czyszczenie ID
        empik_df['ID']   = clean_id_column(empik_df['ID'])
        allegro_df['ID'] = clean_id_column(allegro_df['ID'])

        st.success("Pliki poprawnie wczytane i znormalizowane!")
        st.subheader("Empik (lista ID do aktualizacji)")
        st.dataframe(empik_df[['ID']].head())

        st.subheader("Allegro (źródło prawdy: ID, Cena, Ilość)")
        st.dataframe(allegro_df.head())

        # 3️⃣ LEFT JOIN na ID
        result = pd.merge(empik_df[['ID']],
                          allegro_df,
                          on='ID',
                          how='left')

        # 4️⃣ Uzupełniamy brakujące
        result['Cena'] = result['Cena'].fillna(0)
        result['Ilość'] = result['Ilość'].fillna(0).astype(int)

        st.subheader("Wynik aktualizacji")
        st.dataframe(result.head())

        # 5️⃣ Przygotowanie do pobrania
        @st.cache_data
        def to_excel(df: pd.DataFrame) -> bytes:
            from io import BytesIO
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as w:
                df.to_excel(w, index=False)
            return out.getvalue()

        excel_bytes = to_excel(result)
        st.download_button("📥 Pobierz wynik (.xlsx)",
                           data=excel_bytes,
                           file_name="wynik.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Błąd przetwarzania plików:\n{e}")
else:
    st.warning("⚠️ Wgraj oba pliki (Empik i Allegro), aby rozpocząć.")
