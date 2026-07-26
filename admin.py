import streamlit as st
import pandas as pd
from supabase_client import supabase
def show(df):
    st.title(":material/admin_panel_settings: Admin Panel")

    st.divider()

    st.subheader(":material/settings: System Status")

    try:

        response = (
        supabase
        .table("call_logs")
        .select("*", count="exact")
        .execute()
    )

    total_logs = response.count

    st.success("Supabase Connected")

    st.info(f"Total Call Logs : {total_logs}")

        except:

         st.error("Supabase Connection Failed")
     st.divider()

     st.subheader(":material/upload_file: Portfolio Management")

      uploaded_portfolio = st.file_uploader(

    "Upload New Motor Portfolio",

    type=["xlsx"]

)

    if uploaded_portfolio:

        portfolio = pd.read_excel(uploaded_portfolio)

        st.success(

        f"{len(portfolio)} policies loaded."

    )

        st.dataframe(

        portfolio.head()

    )

        st.info(

        "This portfolio can replace the existing renewal portfolio after validation."

    )
    st.divider()

    st.subheader(":material/download: Data Management")

response = (

    supabase

    .table("call_logs")

    .select("*")

    .execute()

)

logs = pd.DataFrame(response.data)

   st.download_button(

     "Download Call Logs",

      logs.to_csv(index=False),

    file_name="call_logs.csv",

    mime="text/csv"

)
    st.divider()

    st.subheader(":material/info: System Information")

    st.write("CRM Version : 1.0")

    st.write("Developer : Milliano Benjamin Kadzilawa")

    st.write("Database : Supabase")

    st.write("Application : Motor Renewal CRM")
  
