"""Step 3 (collect): Public form that writes to a private Google Sheet.

This app is deployed without a login — anyone with the URL can submit. It
writes to a sheet via a service account whose credentials live in Streamlit
Cloud's Secrets panel (never in this file).

Before deploying:
  1. Follow docs/03-service-account-setup.md to create a service account
     and share your sheet with it.
  2. On Streamlit Cloud, paste your service-account JSON fields, sheet_id,
     and admin_password into the app's Secrets panel using the shape in
     .streamlit/secrets.toml.example.

Expected sheet header row:
  timestamp | workshop | rating | comments | status
"""

import datetime as dt

import gspread
import streamlit as st


@st.cache_resource
def get_worksheet():
    creds = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(creds)
    return client.open_by_key(st.secrets["sheet_id"]).sheet1


st.set_page_config(page_title="Submit feedback", page_icon="📝")
st.title("📝 Workshop feedback")
st.caption("Your response is saved to our records. Thanks!")

with st.form("feedback_form", clear_on_submit=True):
    workshop = st.text_input("Workshop name")
    rating = st.slider("Rating", 1, 5, 4)
    comments = st.text_area("Comments", placeholder="Optional")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not workshop:
            st.error("Workshop name is required.")
        else:
            try:
                ws = get_worksheet()
                ws.append_row([
                    dt.datetime.now().isoformat(timespec="seconds"),
                    workshop,
                    int(rating),
                    comments,
                    "new",
                ])
                st.success("Thanks! Your feedback was recorded.")
            except Exception as e:
                st.error(f"Couldn't save: {e}")
