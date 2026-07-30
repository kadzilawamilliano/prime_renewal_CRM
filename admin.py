import streamlit as st
import pandas as pd

from supabase_client import supabase
from migration_calls import migrate_calls


def show(df):

    st.title(":material/admin_panel_settings: Admin Panel")

    # =====================================
    # SYSTEM STATUS
    # =====================================

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

        st.success("🟢 Supabase Connected")

        st.info(f"Total Call Logs: {total_logs}")

    except Exception:

        st.error("🔴 Supabase Connection Failed")

    # =====================================
    # PORTFOLIO MANAGEMENT
    # =====================================

    st.divider()

    st.subheader(":material/upload_file: Portfolio Management")

    uploaded_portfolio = st.file_uploader(

        "Upload New Motor Portfolio",

        type=["xlsx"]

    )

    if uploaded_portfolio:

        portfolio = pd.read_excel(uploaded_portfolio)

        st.success(f"{len(portfolio)} policies loaded.")

        st.dataframe(portfolio.head())

        st.info(

            "This portfolio can replace the existing renewal portfolio after validation."

        )

    # =====================================
    # HISTORICAL CALL MIGRATION
    # =====================================

    st.divider()

    st.subheader(":material/cloud_upload: Historical Call Migration")

    st.warning(
        "This imports historical call records from motor_renewals_tracking.xlsx into Supabase."
    )

    confirm = st.checkbox(
        "I understand this is a one-time migration."
    )

    if confirm:

        if st.button("Import Historical Calls"):

            with st.spinner("Importing historical call history..."):

                uploaded, skipped = migrate_calls()

            st.success("Migration Completed Successfully!")

            st.write(f"Uploaded Records : {uploaded}")

            st.write(f"Skipped Duplicates : {skipped}")

            st.balloons()

    # =====================================
    # DATA MANAGEMENT
    # =====================================

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

    # =====================================
    # SYSTEM INFORMATION
    # =====================================

    st.divider()

    st.subheader(":material/info: System Information")

    st.write("CRM Version : 1.0")

    st.write("Developer : Milliano Benjamin Kadzilawa")

    st.write("Database : Supabase")

    st.write("Application : Motor Renewal CRM")
