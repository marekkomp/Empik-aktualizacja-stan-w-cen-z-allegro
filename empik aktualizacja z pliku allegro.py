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

# 1) Upload plików
empik_file = st.file_uploader("📤 Wgraj plik EMPiK (.xlsx)", type=["xlsx"])
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
        # 2) Wczytaj plik EMPiK (ID jako tekst)
        empik_df = pd.read_excel(
            empik_file,
            usecols=[0], header=None, names=['ID'], engine='openpyxl', dtype=str
        ).fillna('')

        # 3) Wczytaj plik ALLEGRO (surowe wartości)
        allegro_df = pd.read_excel(
            allegro_file,
            usecols=[0,1,2], header=None, names=['ID','Cena','Ilość'], engine='openpyxl'
        ).fillna('')

        # 4) Normalizacja ID w obu DataFrame
        empik_df['ID'] = clean_id_column(empik_df['ID'])
        allegro_df['ID'] = clean_id_column(allegro_df['ID'])

        # 5) Ujednolicenie formatu liczbowego dla kolumn Cena i Ilość
        for col in ['Cena', 'Ilość']:
            # Zamiana przecinków na kropki oraz rzutowanie na string
            serie = allegro_df[col].astype(str).str.replace(',', '.', regex=True)
            # Konwersja na liczbę zmiennoprzecinkową
            num = pd.to_numeric(serie, errors='coerce').fillna(0)
            # Ilość jako int, Cena jako float
            allegro_df[col] = num.astype(int) if col == 'Ilość' else num

        st.success("✅ Pliki poprawnie wczytane i znormalizowane!")
        st.subheader("Empik (lista ID do aktualizacji)")
        st.dataframe(empik_df)

        st.subheader("Allegro (źródło prawdy: ID, Cena, Ilość)")
        st.dataframe(allegro_df)

        # 6) LEFT JOIN → wszystkie ID z Empik
        result = pd.merge(empik_df, allegro_df, on='ID', how='left')

        # 7) Uzupełnienie braków zerami
        result['Cena'] = result['Cena'].fillna(0)
        result['Ilość'] = result['Ilość'].fillna(0).astype(int)

        st.subheader("Wynik aktualizacji")
        st.dataframe(result)

        # 8) Przygotowanie do pobrania
        @st.cache_data
        def to_excel(df: pd.DataFrame) -> bytes:
            from io import BytesIO
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return out.getvalue()

        st.download_button(
            "📥 Pobierz wynik (.xlsx)",
            data=to_excel(result),
            file_name="wynik.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Błąd przetwarzania plików:\n{e}")
else:
    st.warning("⚠️ Wgraj oba pliki (Empik i Allegro), aby rozpocząć.")
