import streamlit as st
import pandas as pd
import urllib.parse
import re
conn = sqlite3.connect("crm.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    reg_number TEXT,
    status TEXT,
    feedback TEXT
)
""")

conn.commit()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

conn.commit()

def create_default_users():
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", "admin123", "admin"))

    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("agent1", "pass1", "agent"))

    conn.commit()

create_default_users()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


import streamlit as st

def login():
    st.title("🔐 CRM Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user[3]  # role column

            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
            if "logged_in" not in st.session_state:v.    
                st.session_state.logged_in = False
def main_app():
    
st.title("🚗 Motor Renewal CRM")

st.write(f"Welcome {st.session_state.username} ({st.session_state.role})")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.success("CRM Dashboard goes here")
    if st.session_state.logged_in:
    main_app()
else:
    login()




st.set_page_config(page_title="Motor Renewal CRM", layout="wide")

st.title("🚗 Motor Renewal Retention CRM")
st.caption("Built by Milliano Benjamin Kadzilawa")

# =========================
# LOAD DATA
# =========================

FILE_PATH = "motor_renewals_tracking_sample.xlsx"

try:
    df = pd.read_excel(FILE_PATH)
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

# Convert renewal date
df["Renewal Date"] = pd.to_datetime(df["Renewal Date"])

# Session storage
if "call_logs" not in st.session_state:
    st.session_state.call_logs = {}

# =========================
# SEARCH CLIENT
# =========================

search = st.text_input("🔍 Search Client")

if search:
    filtered_df = df[
        df.astype(str)
        .apply(lambda x: x.str.contains(search, case=False, na=False))
        .any(axis=1)
    ]
else:
    filtered_df = df

if filtered_df.empty:
    st.warning("No matching client found.")
    st.stop()

client = st.selectbox(
    "Select Client",
    filtered_df["Policy Holder"].unique()
)

row = filtered_df[
    filtered_df["Policy Holder"] == client
].iloc[0]

# =========================
# CLIENT DETAILS
# =========================

st.subheader("📄 Client Details")

st.write("**Policy Holder:**", row["Policy Holder"])
st.write("**Phone:**", row["Phone Number"])
st.write("**Renewal Date:**", row["Renewal Date"].strftime("%d %B %Y"))

# =========================
# PHONE
# =========================

phone = str(row["Phone Number"])
phone = re.sub(r"\D", "", phone)

if phone.startswith("0"):
    whatsapp_phone = "265" + phone[1:]
elif phone.startswith("265"):
    whatsapp_phone = phone
else:
    whatsapp_phone = phone

st.markdown(
    f"[📞 Call Client](tel:{phone})"
)

# =========================
# WHATSAPP
# =========================

expiry = row["Renewal Date"] - pd.Timedelta(days=1)

message = f"""
Hello {row['Policy Holder']},

My name is Milliano Kadzilawa from Prime Insurance Company.

This is a reminder that your insurance policy for your vehicle is due to expire on {expiry.strftime('%d %B %Y')}.

Please visit any Prime Insurance office or contact your broker to renew.

Thank you for choosing Prime Insurance.
"""

encoded = urllib.parse.quote(message)

whatsapp_url = (
    f"https://wa.me/{whatsapp_phone}?text={encoded}"
)

st.markdown(
    f"[💬 WhatsApp Client]({whatsapp_url})"
)

# =========================
# CALL OUTCOME
# =========================

st.subheader("📞 Call Outcome")

outcome = st.selectbox(
    "Outcome",
    [
        "No Answer",
        "Busy",
        "Wrong Number",
        "Will Renew",
        "Pending Decision",
        "Not Interested",
        "Renewed Already",
        "Not Reachable",
        "Invalid Number"
    ]
)

notes = st.text_area("Call Notes")

# =========================
# SAVE
# =========================

if st.button("💾 Save Call Record"):

    st.session_state.call_logs[row["Policy Number"]] = {

        "Policy Holder": row["Policy Holder"],
        "Policy Number": row["Policy Number"],
        "Vehicle": row["Vehicle Registration"],
        "Phone": row["Phone Number"],
        "Outcome": outcome,
        "Notes": notes,
        "Renewal Date": row["Renewal Date"]

    }

    st.success("Call record saved for this session.")

# =========================
# CALL HISTORY
# =========================

st.markdown("---")
st.subheader("📊 Call History")

if st.session_state.call_logs:

    history = pd.DataFrame(
        st.session_state.call_logs.values()
    )

    st.dataframe(history, use_container_width=True)

else:

    st.info("No call records yet.")
