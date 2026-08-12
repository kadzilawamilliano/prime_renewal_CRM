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
        # =====================================
    # DATA MANAGEMENT
    # =====================================

    st.divider()

    st.subheader(":material/download: Data Management")

    # Date filters

    from_date = st.date_input(
        "Call Date From"
    )

    to_date = st.date_input(
        "Call Date To"
    )


    # Call Status filter

    call_status_filter = st.selectbox(
        "Call Status",
        [
            "All",
            "Renewed",
            "Will Renew",
            "Pending Decision",
            "No Answer",
            "Busy",
            "Wrong Number",
            "Not Interested",
            "Not Reachable"
        ]
    )


    # WhatsApp Status filter

    whatsapp_filter = st.selectbox(
        "WhatsApp Status",
        [
            "All",
            "Not Checked",
            "Message Sent",
            "No WhatsApp",
            "Failed"
        ]
    )


    # Build query

    query = (
        supabase
        .table("call_logs")
        .select("*")
        .gte("call_date", str(from_date))
        .lte("call_date", str(to_date))
    )


    if call_status_filter != "All":

        query = query.eq(
            "call_status",
            call_status_filter
        )


    if whatsapp_filter != "All":

        query = query.eq(
            "whatsapp_status",
            whatsapp_filter
        )


    response = query.execute()

    logs = pd.DataFrame(response.data)


    st.info(
        f"Matching Records: {len(logs)}"
    )


    if not logs.empty:

        st.download_button(
            "📥 Download Call Logs",
            logs.to_csv(index=False),
            file_name=(
                f"call_logs_"
                f"{from_date}_"
                f"to_{to_date}.csv"
            ),
            mime="text/csv"
        )

    else:

        st.warning(
            "No call logs found for the selected filters."
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
