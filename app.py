import streamlit as st
import pandas as pd

from pages.dashboard import show_dashboard
from pages.client_management import show_client_management

from supabase_client import supabase
import admin
import report


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Motor Renewal CRM",
    page_icon=":material/directions_car:",
    layout="wide"
)


# =====================================
# HEADER
# =====================================

st.title(":material/directions_car: Motor Renewal Retention CRM System")

st.caption(
    "Built by Milliano Benjamin Kadzilawa"
)


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title(":material/menu: Navigation")

page = st.sidebar.radio(

    "Go To",

    [

        "Dashboard",

        "Client Management",

        "Reports",

        "Admin"

    ]

)


# =====================================
# LOAD EXCEL DATA
# =====================================

FILE_PATH = "motor_renewals_tracking.xlsx"


@st.cache_data
def load_data():

    df = pd.read_excel(FILE_PATH)

    df.columns = df.columns.str.strip()

    date_columns = [

        "Commencement Date",

        "Renewal Date",

        "Call Date",

        "Next Follow Up"

    ]

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


# =====================================
# CHECK SUPABASE CONNECTION
# =====================================

try:

    supabase.table("call_logs").select("*").limit(1).execute()

    st.sidebar.success("Supabase Connected")

except Exception:

    st.sidebar.error("Supabase Connection Failed")


# =====================================
# PAGE NAVIGATION
# =====================================

if page == "Dashboard":

    show_dashboard(df)

elif page == "Client Management":

    show_client_management(df)

elif page == "Reports":
    report.show(df)

    st.header(":material/assessment: Reports")

    #st.info("Reports module coming next.")

elif page == "Admin":
    admin.show(df)

    #st.header(":material/admin_panel_settings: Admin")

    #st.info("Admin module coming next.")
