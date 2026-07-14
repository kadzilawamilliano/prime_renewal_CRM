import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import urllib.parse
import re


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
# EXCEL DATA SOURCE
# =====================================

# Excel file must be uploaded to GitHub repository
FILE_PATH = "motor_renewals_tracking.xlsx"


@st.cache_data
def load_data():

    df = pd.read_excel(FILE_PATH)


    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
    )


    # Convert dates
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
# DATABASE CONNECTION
# =====================================


conn = sqlite3.connect(
    "crm.db",
    check_same_thread=False
)


cursor = conn.cursor()



# =====================================
# CREATE CALL LOG TABLE
# =====================================
# =====================================
# ANALYTICS DATABASE STRUCTURE
# =====================================


cursor.execute("""

CREATE TABLE IF NOT EXISTS call_logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    policy_number TEXT,

    policy_holder TEXT,

    premium REAL,

    call_date TEXT,

    call_status TEXT,

    feedback TEXT,

    next_follow_up TEXT,

    renewed TEXT,

    user TEXT

)

""")


conn.commit()

# =====================================
# SAVE CALL RECORD FUNCTION
# =====================================
# =====================================
# SAVE CALL ACTIVITY
# =====================================


def save_call_record(

    policy_number,

    policy_holder,

    premium,

    call_status,

    feedback,

    next_follow_up,

    renewed,

    user="Milliano"

):


    cursor.execute("""

    INSERT INTO call_logs

    (

    policy_number,
    policy_holder,
    premium,
    call_date,
    call_status,
    feedback,
    next_follow_up,
    renewed,
    user

    )


    VALUES(?,?,?,?,?,?,?,?,?)

    """,

    (

    policy_number,

    policy_holder,

    premium,

    datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    ),

    call_status,

    feedback,

    next_follow_up,

    renewed,

    user

    ))


    conn.commit()

# =====================================
# LOAD CALL HISTORY
# =====================================


def load_call_history():

    history = pd.read_sql_query(

        """
        SELECT *
        FROM call_logs
        """,

        conn

    )


    return history



history = load_call_history()



# =====================================
# MERGE ORIGINAL DATA WITH DATABASE
# =====================================


if not history.empty:


    df = df.merge(

        history,

        how="left",

        left_on="Policy Number",

        right_on="policy_number"

            )
    # =====================================
# PHASE 2
# CLIENT SEARCH & PROFILE
# =====================================


st.divider()


st.subheader(
    ":material/search: Search Client"
)


# Create searchable text box

search = st.text_input(
    "Search by Policy Holder, Policy Number or Vehicle Registration"
)



# =====================================
# FILTER DATA
# =====================================


if search:


    search_result = df[

        df.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search,
                case=False,
                na=False
            ).any(),

            axis=1
        )

    ]


else:

    search_result = df



# Check if data exists

if search_result.empty:

    st.warning(
        "No client found."
    )

    st.stop()



# =====================================
# SELECT CLIENT
# =====================================


client_list = (

    search_result["Policy Holder"]
    .dropna()
    .unique()

)


selected_client = st.selectbox(

    ":material/person_search: Select Client",

    client_list

)



# Get selected client record

client = search_result[

    search_result["Policy Holder"]
    ==
    selected_client

].iloc[0]



# =====================================
# CLIENT PROFILE
# =====================================


st.divider()


st.subheader(
    ":material/person: Client Details"
)



col1, col2 = st.columns(2)



with col1:


    st.write(
        ":material/description: **Policy Number**"
    )

    st.info(
        client["Policy Number"]
    )


    st.write(
        ":material/person: **Policy Holder**"
    )

    st.info(
        client["Policy Holder"]
    )


    st.write(
        ":material/directions_car: **Vehicle Registration**"
    )

    st.info(
        client["Vehicle Registration"]
    )



with col2:


    st.write(
        ":material/payments: **Premium**"
    )
    

st.info(
        client["Premium"]
    )


st.write(
    ":material/event: **Commencement Date**"
    )

st.info(
        client["Commencement Date"]
    )


st.write(
        ":material/event_available: **Renewal Date**"
    )

st.info(
        client["Renewal Date"]
    )



# Save selected client for next phases

st.session_state["selected_client"] = client
# =====================================
# PHASE 3
# CALL & WHATSAPP ACTIONS
# =====================================


st.divider()


st.subheader(
    ":material/communication: Client Communication"
)



# Get selected client

client = st.session_state["selected_client"]



# =====================================
# PHONE NUMBER PROCESSING
# =====================================


phone = str(
    client.get("Phone Number", "")
)


# Remove spaces and symbols

phone = re.sub(
    r"\D",
    "",
    phone
)



# Convert Malawi international format

if phone.startswith("265"):

    local_phone = "0" + phone[3:]

else:

    local_phone = phone



# WhatsApp format

whatsapp_phone = local_phone


if whatsapp_phone.startswith("0"):

    whatsapp_phone = (
        "265" +
        whatsapp_phone[1:]
    )



# =====================================
# RENEWAL EXPIRY DATE
# =====================================


renewal_date = pd.to_datetime(

    client["Renewal Date"],

    errors="coerce"

)


expiry_date = (
    renewal_date -
    pd.Timedelta(days=1)
)



expiry_date_text = expiry_date.strftime(
    "%d %B %Y"
)



# =====================================
# MESSAGE TEMPLATE
# =====================================


name = client["Policy Holder"]

vehicle = client["Vehicle Registration"]



message = f"""

Hello {name},

My name is Milliano Kadzilawa from Prime Insurance Company.

This is a reminder that your insurance policy for vehicle {vehicle} is expected to expire on {expiry_date_text}.

We kindly encourage you to renew your insurance through our agents or visit our office directly.

Thank you for trusting Prime Insurance Company.

"""



# Encode WhatsApp message

encoded_message = urllib.parse.quote(
    message
)



whatsapp_url = (

    f"https://wa.me/"
    f"{whatsapp_phone}"
    f"?text={encoded_message}"

)



# =====================================
# ACTION BUTTONS
# =====================================


col1, col2 = st.columns(2)



with col1:


    st.link_button(

        ":material/phone: Call Client",

        f"tel:{local_phone}"

    )



with col2:


    st.link_button(

        ":material/chat: WhatsApp Client",

        whatsapp_url

    )



# =====================================
# DISPLAY CONTACT DETAILS
# =====================================


st.write(
    ":material/smartphone: Phone Number:",
    local_phone
)


st.write(
    ":material/event_busy: Expected Expiry Date:",
    expiry_date_text
    )
# =====================================
# PHASE 4
# CALL OUTCOME & SAVE RECORD
# =====================================

st.divider()

st.subheader(":material/edit_note: Call Outcome")

# Get selected client
client = st.session_state["selected_client"]


# -------------------------------------
# Call Status
# -------------------------------------

call_status = st.selectbox(

    "Call Status",

    [

        "No Answer",
        "Busy",
        "Wrong Number",
        "Will Renew",
        "Pending Decision",
        "Not Interested",
        "Renewed Already",
        "Not Reachable",
        "Will Not Renew",
        "Invalid Number"

    ]

)


# -------------------------------------
# Feedback
# -------------------------------------

feedback = st.text_area(

    "Feedback / Notes",

    height=120

)


# -------------------------------------
# Next Follow Up
# -------------------------------------

next_follow_up = st.date_input(

    "Next Follow Up Date",

    value=datetime.today()

)


# -------------------------------------
# Renewed
# -------------------------------------

renewed = st.selectbox(

    "Policy Renewed?",

    [

        "No",
        "Yes"

    ]

)

# -------------------------------------
# Save Button
# -------------------------------------

if st.button(
    ":material/save: Save Call Record",
    use_container_width=True
):
    save_call_record(
        policy_number=client["Policy Number"],
        policy_holder=client["Policy Holder"],
        premium=client["Premium"],
        call_status=call_status,
        feedback=feedback,
        next_follow_up=str(next_follow_up),
        renewed=renewed
    )

    st.success(
        "Call record saved successfully."
    )

    st.rerun()

# =====================================
# PHASE 5
# CLIENT ACTIVITY TIMELINE
# =====================================

st.divider()

st.subheader(
    ":material/history: Client Activity Timeline"
)


history = pd.read_sql_query(

    """

    SELECT *

    FROM call_logs

    WHERE policy_number = ?

    ORDER BY id DESC

    """,

    conn,

    params=(client["Policy Number"],)

)


if history.empty:

    st.info(
        "No activities recorded for this client."
    )

else:

    for _, record in history.iterrows():

        with st.container(border=True):

            st.markdown(
                f"### :material/phone_in_talk: {record['call_date']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Call Status**"
                )

                st.success(
                    record["call_status"]
                )

            with col2:

                st.write(
                    "**Renewed**"
                )

                if record["renewed"] == "Yes":

                    st.success("YES")

                else:

                    st.warning("NO")


            st.write(
                "**Feedback**"
            )

            st.info(
                record["feedback"]
            )


            st.write(
                "**Next Follow Up**"
            )

            st.write(
                record["next_follow_up"]
            )


            st.write(
                "**Officer**"
            )

            st.write(
                record["user"]
            )
