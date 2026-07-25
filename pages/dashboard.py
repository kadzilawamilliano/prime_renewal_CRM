import streamlit as st
import pandas as pd

from utils.database import (
    get_all_call_logs
)

from utils.analytics import (
    calculate_kpis,
    daily_calls,
    weekly_calls,
    monthly_calls
)

from supabase_client import supabase
def show_dashboard(df):

    st.header(":material/dashboard: Executive Dashboard")

    dashboard = get_all_call_logs()
        kpis = calculate_kpis(df, dashboard)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Clients",
        kpis["total_clients"]
    )

    c2.metric(
        "Calls Made",
        kpis["total_calls"]
    )

    c3.metric(
        "Renewed",
        kpis["renewed_clients"]
    )

    c4.metric(
        "Retention %",
        f"{kpis['retention_rate']}%"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Portfolio Premium",
        f"MWK {kpis['portfolio_premium']:,.0f}"
    )

    c2.metric(
        "Retained Premium",
        f"MWK {kpis['retained_premium']:,.0f}"
    )

    c3.metric(
        "Pending Follow-up",
        kpis["pending_followups"]
    )
        st.divider()

    st.subheader(
        ":material/analytics: Activity Summary"
    )

    a, b, c = st.columns(3)

    a.metric(
        "Today",
        daily_calls(dashboard)
    )

    b.metric(
        "Last 7 Days",
        weekly_calls(dashboard)
    )

    c.metric(
        "This Month",
        monthly_calls(dashboard)
    )
        st.divider()

    st.subheader(
        ":material/upload_file: Verify Renewed Policies"
    )

    uploaded_file = st.file_uploader(

        "Upload Official Renewed Policies",

        type=["xlsx"]

    )
    

