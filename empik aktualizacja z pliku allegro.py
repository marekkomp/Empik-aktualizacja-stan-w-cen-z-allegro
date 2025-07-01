import streamlit as st
import pandas as pd

st.title("Empik – aktualizacja z pliku Allegro")

st.info("""
ℹ️ Wymagany format plików Excel (.xlsx):  
- Nagłówek w pierwszym wierszu: **ID | Cena | Ilość**  
- Kolumna A = ID  
- Kolumna B = Cena  
- Kolumna C = Ilość
""")

# 1️⃣ Upload plików
empik_file = st.file_uploader("Wgraj plik EMPIK (.xlsx)", type=["xlsx"])
allegro_file = st.file_uploader("Wgraj plik ALLEGRO (.xlsx)", type=["xlsx"])

if empik_file and allegro_file:
    try:
        # 2️⃣ Wczytanie danych
        empik_df = pd.read_excel(empik_file)
        allegro_df = pd.read_excel(allegro_file)

        st.success("✅ Pliki zostały wczytane poprawnie!")

        st.subheader("Podgląd – Empik")
        st.dataframe(empik_df)

        st.subheader("Podgląd – Allegro")
        st.dataframe(allegro_df)

        # 3️⃣ Join – tylko kolumna ID z Empik, dane z Allegro
        result = pd.merge(
            empik_df[['ID']],
            allegro_df,
            on='ID',
            how='left'
        )

        # 4️⃣ Uzupełnienie braków
        result['Cena'] = result['Cena'].fillna(0)
        result['Ilość'] = result['Ilość'].fillna(0).astype(int)

        st.subheader("✅ Wynik")
        st.dataframe(result)

        # 5️⃣ Export do Excel
        @st.cache_data
        def to_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            processed_data = output.getvalue()
            return processed_data

        excel_data = to_excel(result)
        st.download_button(
            label="📥 Pobierz wynik (.xlsx)",
            data=excel_data,
            file_name='wynik.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        st.error(f"Błąd przetwarzania plików: {e}")

else:
    st.warning("⚠️ Wgraj oba pliki, żeby kontynuować.")
