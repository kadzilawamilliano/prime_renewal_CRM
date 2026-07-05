import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("crm.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_number TEXT,
    vehicle_reg TEXT,
    premium TEXT,
    phone_numbe TEXT,
    policy_holder TEXT,
    commencement_date TEXT,
    expiry_date TEXT,
    renewal_date TEXT,
    notes TEXT,
    call_status TEXT,
    call_date TEXT
)
""")

conn.commit()
st.write("database connected")
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
st.write(c.fetchall())
# =========================
# DEFAULT USER
# =========================
def create_users():
    c.execute("INSERT OR IGNORE INTO users (username,password,role) VALUES (?,?,?)",
              ("admin", "admin123", "admin"))
    conn.commit()

create_users()

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# LOGIN
# =========================
def login():
    st.title("🔐 Insurance CRM Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# =========================
# WHATSAPP MESSAGE
# =================

# =========================
# IMPORT EXCEL
# =========================
def upload_data():
    st.subheader("📂 Import Motor Renewal Data")
import os
st.write("Current folder:",
os.getcwd())
st.write("Files in folder:")
st.write(os.listdir())
df=pd.read_excel("motor_renewals_tracking.xlsx")

st.success(f"Dataset loaded successfully! ({len(df)} records)")
st.dataframe(df.head())

if st.button("Import into CRM"):

            # Clear old records before importing
            c.execute("DELETE FROM clients")

            for _, row in df.iterrows():
                c.execute("""
                INSERT INTO clients (
                    policy_number,
                    policy_holder,
                    vehicle_reg,
                    phone_number,
                    renewal_date,
                    notes,
                    call_status,
                    call_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row.get("Policy Number", "")),
                    str(row.get("Policy Holder", "")),
                   str(row.get("Vehicle Registration", "")),
                    str(row.get("Phone Number")),
                    str(row.get("Renewal Date", "")),
                    str(row.get("Feedback", "")),
                    str(row.get("Call Status", "Pending")),
                    str(row.get("Call Date", ""))
                ))

            conn.commit()
            st.success("✅ All records imported successfully!")

#except FileNotFoundError:
st.error("❌ motor_renewal_tracking.xlsx was not found.")
# =========================
# SEARCH
# =========================

# =========================
# RENEWAL TYPE
# =========================
def renewal_type(comm, exp):
    try:
        d1 = datetime.strptime(str(comm), "%Y-%m-%d")
        d2 = datetime.strptime(str(exp), "%Y-%m-%d")

        months = (d2 - d1).days / 30

        return "Extension" if months <= 3 else "Full Renewal"
    except:
        return "Unknown"

# =========================
# CLIENT ACTIONS
import streamlit as st
import pandas as pd

# =============================
# LOAD DATA
# =============================
import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import re
from datetime import datetime

# =============================
# DATABASE
# =============================
conn = sqlite3.connect("crm.db", check_same_thread=False)
c = conn.cursor()

# =============================
# LOAD CLIENTS
# =============================
df = pd.read_sql_query("SELECT * FROM clients", conn)
# =============================
# SESSION STORAGE (CALL LOGS)
# =============================

# =============================
# STEP 1: SELECT CLIENT
# =============================
# =============================
# STEP 1: SEARCH & SELECT CLIENT
# ======================
# =============================
# SEARCH CLIENT
# =============================

search = st.text_input(
    "🔍 Search Client (Policy Number / Name / Vehicle)"
)

if search:
    filtered_df = df[
        df.astype(str)
        .apply(lambda x: x.str.contains(search, case=False, na=False))
        .any(axis=1)
    ]
else:
    filtered_df = df

if filtered_df.empty:
    st.warning("No client found.")
    st.stop()

client = st.selectbox(
    "Select Client",
    filtered_df["policy_holder"].unique()
)

row = filtered_df[
    filtered_df["policy_holder"] == client
].iloc[0]
# =============================
st.subheader("📄 Client Details")
#St.write(f"Policy Number: {row['Policy_number'])
#
#st.write(f"📄 Policy Holder: {row['Policy_holder']}")


st.write(f"🚘 Vehicle: {row['Vehicle_reg']}")


st.write(f"📞 Phone: {row['Phone_number']}")


st.write(f"📅 Renewal Date: {row['renewal_date']}")


# =============================
# STEP 3: CALL / WHATSAPP
# =============================
#phone = str(row["Phone Number"]).strip()

#st.markdown(
   # f"📞 [Call Client](tel:{phone})",
  #  unsafe_allow_html=True
#)

#st.markdown(
  #  f"💬 [WhatsApp Client](https://wa.me/{phone})",
   # unsafe_allow_html=True
#)
# ===============
import urllib.parse

import streamlit as st

import pandas as pd



phone = str(row["Phone Number"]).strip()

reg_number = row["Vehicle Registration"]

Name = row["Policy Holder"]

import re

phone = str(row["Phone Number"])
phone = re.sub(r"\D", "", phone)  # Remove spaces and other non-digit characters

# Convert international format (265...) to local format (0...)
if phone.startswith("265"):
    phone = "0" + phone[3:]

st.markdown(
  f"📞 [Call Client](tel:{phone})",
     unsafe_allow_html=True
    )
# Convert renewal date to datetime

renewal_date = pd.to_datetime(row["Renewal Date"])


# Compute expiry date (1 day before renewal)
expiry_date = renewal_date - pd.Timedelta(days=1)

expiry_date = renewal_date - pd.Timedelta(days=1)



# Format date nicely

expiry_date_str = expiry_date.strftime("%d %B %Y")

message = f"""
Hello, {Name}

My name is Milliano Kadzilawa, I'm from Prime Insurance Company.

This is a reminder that your insurance policy for vehicle {reg_number} is about to expire on {expiry_date_str}.

We kindly encourage you to renew your insurance through our agents or visit our office directly.

Thank you for trusting Prime Insurance Company.
"""
import re

phone = str(row["Phone Number"])
phone = re.sub(r"\D", "", phone)

if phone.startswith("0"):
    phone = "265" + phone[1:]

st.write("Phone:", phone)
st.write("WhatsApp URL:", f"https://wa.me/{phone}")


encoded = urllib.parse.quote(message)

whatsapp_url = f"https://wa.me/{phone}?text={encoded}"

st.markdown(f"[💬 WhatsApp Client]({whatsapp_url})", unsafe_allow_html=True)
# =============================
# STEP 4: CALL OUTCOME
# =============================
st.subheader("📞 Call Outcome")

outcome = st.selectbox(
    "Select outcome",
    [
        "No Answer",
        "Busy",
        "Wrong Number",
        "Will Renew",
        "Pending Decision",
        "Not Interested",
        "Renewed Already",
        "Not reachable",
        "Invalid number"
    ],
    key=f"outcome_{row['Policy Number']}"
)

notes = st.text_area(
    "Call Notes",
    key=f"notes_{row['Policy Number']}"
)

# =============================
# STEP 5: SAVE BUTTON
# =============================
st.session_state.call_logs[row["Policy Number"]] = {
    "Policy Holder": row["Policy Holder"],
    "Policy Number": row["Policy Number"],
    "Vehicle": row["Vehicle Registration"],
    "Phone": row["Phone Number"],
    "Outcome": outcome,
    "Notes": notes,
    "Renewal Date": row["Renewal Date"]
}

#save permanently

FILE_PATH = "/content/drive/MyDrive/Renewals/motor_renewals_tracking.xlsx"

df = pd.read_excel(FILE_PATH)

from datetime import datetime

if st.button("💾 Save Call Record", key=f"save_{row['Policy Number']}"):

    mask = df["Policy Number"] == row["Policy Number"]

    df.loc[mask, "Call Date"] = datetime.now().strftime("%d-%m-%Y")
    df.loc[mask, "Call Status"] = outcome
    df.loc[mask, "Feedback"] = notes

    df.to_excel(FILE_PATH, index=False)

    st.success("✅ Call record saved successfully!")
# =============================
# STEP 6: CALL HISTORY
# =============================
st.markdown("---")
st.subheader("📊 Call History")

if st.session_state.call_logs:

    for policy, data in st.session_state.call_logs.items():

        st.write(f"👤 {data['Policy Holder']}")
        st.write(f"📄 Policy: {data['Policy Number']}")
        st.write(f"🎯 Outcome: {data['Outcome']}")
        st.write(f"📝 Notes: {data['Notes']}")
        st.write(f"📞 Phone: {data['Phone']}")
        st.divider()

else:
    st.info("No call records yet.")


# =========================

# =========================
# MAIN APP
# =========================
def main_app():
    st.title("🚗 Insurance CRM System")

    st.write(f"Welcome **{st.session_state.user}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    upload_data()
    search_clients()
    client_actions()
    view_clients()

# =========================
# FLOW
# =========================
if not st.session_state.logged_in:
    login()
else:
    main_app()

