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
# =========================
def build_whatsapp_message(name, reg, expiry):
    msg = f"""
Hello, {name}

My name is Milliano Kadzilawa, I'm from Prime Insurance Company.

This is a reminder that your insurance policy for vehicle {reg} is about to expire on {expiry}.

We kindly encourage you to renew your insurance through our agents or visit our office directly.

Thank you for trusting Prime Insurance Company.
"""
    return urllib.parse.quote(msg)

# =========================
# IMPORT EXCEL
# =========================
def upload_data():
    st.subheader("📂 Import Motor Renewal Data")

    try:
        df = pd.read_excel("motor_renewals_tracking.xlsx")

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
                    renewal_date,
                    notes,
                    call_status,
                    call_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.get("Policy Number", ""),
                    row.get("Policy Holder", ""),
                    row.get("Vehicle Registration", ""),
                    row.get("Renewal Date", ""),
                    row.get("Feedback", ""),
                    row.get("Call Status", "Pending"),
                    row.get("Call Date", "")
                ))

            conn.commit()
            st.success("✅ All records imported successfully!")

    except FileNotFoundError:
        st.error("❌ motor_renewal_tracking.xlsx was not found.")
# =========================
# SEARCH
# =========================
def search_clients():
    st.subheader("🔍 Search Client")

    search = st.text_input("Search (Policy / Name / Vehicle Reg)")

    if search:
        c.execute("""
        SELECT * FROM clients
        WHERE policy_number LIKE ?
        OR vehicle_reg LIKE ?
        OR policy_holder LIKE ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))

        results = c.fetchall()

        for r in results:
            st.write(r)

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
# =========================
def client_actions():
    st.subheader("📞 Client Actions")

    c.execute("SELECT id, policy_holder, vehicle_reg, expiry_date FROM clients")
    clients = c.fetchall()

    if not clients:
        st.warning("No clients found")
        return

    for cl in clients:
        cid, name, reg, expiry = cl

        st.write(f"**{name} | {reg}**")

        col1, col2 = st.columns(2)

        # 📞 CALL BUTTON
        with col1:
            if st.button(f"📞 Call {cid}"):
                c.execute("""
                UPDATE clients
                SET call_status=?, call_date=?
                WHERE id=?
                """, ("Called", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cid))

                conn.commit()
                st.success("Marked as Called")

        # 📲 WHATSAPP BUTTON
        with col2:
            msg = build_whatsapp_message(name, reg, expiry)
            url = f"https://wa.me/?text={msg}"

            st.markdown(f'<a href="{url}" target="_blank">📲 WhatsApp</a>',
                        unsafe_allow_html=True)

        st.markdown("---")

# =========================
# VIEW CLIENTS
# =========================
def view_clients():
    st.subheader("📋 Clients")

    c.execute("SELECT * FROM clients")
    data = c.fetchall()

    for r in data:
        st.write(
            f"""
Policy: {r[1]}  
Name: {r[3]}  
Vehicle: {r[2]}  
Status: {r[9]}  
Type: {renewal_type(r[5], r[6])}
"""
        )

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
