import streamlit as st
import pandas as pd
import gspread
import json
from io import StringIO
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets connection from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_data = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)

# Nama Google Sheet & Worksheet (boleh ubah jika perlu)
SHEET_NAME = "SENARAI VALIDASI RMK12 (DH NK HABIS)"
worksheet = client.open(SHEET_NAME).sheet1

# Dapatkan semua data
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Tajuk aplikasi
st.title("Carian Data Berdasarkan NO ASL")

# Input carian
no_asl = st.text_input("Masukkan NO ASL")

if no_asl:
    result = df[df["NO ASL"].astype(str).str.strip() == no_asl.strip()]

    if not result.empty:
        row = result.iloc[0]
        st.success("Maklumat Dijumpai:")
        fields = [
            "FASA", "NEGERI", "NAMA PETANI", "KOD SAMPLE PKK", "ROASTING",
            "LIQUOR", "SENSORY CHOCOLATE 70%", "DATE", "TIME",
            "TEMPERATURE", "COMMENT", "MACHINE", "KOD SENSORY", "SENSORY"
        ]
        for field in fields:
            if field in row:
                st.write(f"**{field}**: {row[field]}")
    else:
        st.error("NO ASL tidak dijumpai.")
