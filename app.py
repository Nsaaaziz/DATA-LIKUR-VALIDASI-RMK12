import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Scope dan autorisasi
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# Akses Google Sheet
sheet = client.open_by_key("1G3Lox_L9Em6mdX1XHZxnGrs_vVIdHzXf")
worksheet = sheet.get_worksheet(0)  # GID pertama
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# UI Streamlit
st.title("🔍 Sistem Carian ID Unik dari Google Sheets")

search_id = st.text_input("Masukkan ID unik (contoh: PRD001):")

if search_id:
    results = df[df.astype(str).apply(lambda row: search_id.lower() in row.astype(str).str.lower().values[0], axis=1)]
    
    if not results.empty:
        st.success(f"{len(results)} hasil dijumpai:")
        st.dataframe(results)
    else:
        st.error("❌ Tiada data dijumpai.")
else:
    st.info("Sila masukkan ID unik untuk mulakan carian.")
