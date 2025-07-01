import streamlit as st
import pandas as pd

st.title("✅ Empik – aktualizacja z pliku Allegro")

st.info("""
ℹ️ Ta aplikacja wymusza zawsze układ kolumn:  
- Kolumna A = ID  
- Kolumna B = Cena  
- Kolumna C = Ilość  
**Nagłówek z pliku jest ignorowany!**
""")

# 1️⃣ Upload plików
empik_file = st.file_uploader("📤 Wgraj plik Empik (.xlsx)", type=["xlsx"])
allegro_file = st.file_uploader("📤 Wgraj plik Allegro (.xlsx)", type=["xlsx"])

if empik_file and allegro_file:
    try:
        # 2️⃣ Wczytaj pliki z wymuszeniem nagłówków
        empik_df = pd.read_excel(empik_file, header=None, names=['ID', 'Cena', 'Ilość'])
        allegro_df = pd.read_excel(allegro_file, header=None, names=['ID', 'Cena', 'Ilość'])

        st.success("✅ Pliki zostały wczytane poprawnie!")
        st.subheader("📌 Empik (ID do aktualizacji):")
        st.dataframe(empik_df)

        st.subheader("📌 Allegro (źródło prawdy):")
        st.dataframe(allegro_df)

        # 3️⃣ Join (LEFT) - zachowaj wszystkie ID z Empik
        result = pd.merge(
            empik_df[['ID']],
            allegro_df,
            on='ID',
            how='left'
        )

        # 4️⃣ Wypełnij brakujące wartości zerami
        result['Cena'] = result['Cena'].fillna(0)
        result['Ilość'] = result['Ilość'].fillna(0).astype(int)

        st.subheader("✅ Wynik:")
        st.dataframe(result)

        # 5️⃣ Eksport do Excel
        @st.cache_data
        def to_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        excel_data = to_excel(result)

        st.download_button(
            label="📥 Pobierz wynik (.xlsx)",
            data=excel_data,
            file_name='wynik.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        st.error(f"❌ Błąd przetwarzania plików: {e}")

else:
    st.warning("⚠️ Wgraj oba pliki .xlsx, żeby kontynuować.")
