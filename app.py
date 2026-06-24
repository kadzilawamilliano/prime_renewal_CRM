import streamlit as st
import sqlite3

# =========================
# DATABASE CONNECTION
# =========================
conn = sqlite3.connect("crm.db", check_same_thread=False)
c = conn.cursor()

# =========================
# CREATE TABLES
# =========================
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
    name TEXT,
    reg_number TEXT,
    status TEXT,
    feedback TEXT
)
""")

conn.commit()

# =========================
# CREATE DEFAULT USERS (RUN ONCE)
# =========================
def create_default_users():
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", "admin123", "admin"))

    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("agent1", "pass1", "agent"))

    conn.commit()

create_default_users()

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

# =========================
# LOGIN FUNCTION
# =========================
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
            st.session_state.role = user[3]

            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# =========================
# VIEW CLIENTS
# =========================
def view_clients():
    st.subheader("📋 Clients")

    c.execute("SELECT id, name, reg_number, status, feedback FROM clients")
    data = c.fetchall()

    for row in data:
        st.write(row)

# =========================
# UPDATE CALL OUTCOME
# =========================
def update_outcome():
    st.subheader("✏️ Update Call Outcome")

    c.execute("SELECT id, name, reg_number FROM clients")
    clients = c.fetchall()

    if not clients:
        st.warning("No clients found in database")
        return

    client_dict = {f"{r[1]} ({r[2]})": r[0] for r in clients}

    selected = st.selectbox("Select Client", list(client_dict.keys()))
    client_id = client_dict[selected]

    status = st.selectbox("Call Status", [
        "Pending", "Called", "No Answer", "Interested", "Not Interested", "Renewed"
    ])

    feedback = st.text_area("Feedback")

    if st.button("💾 Save Outcome"):
        c.execute("""
            UPDATE clients
            SET status = ?, feedback = ?
            WHERE id = ?
        """, (status, feedback, client_id))

        conn.commit()
        st.success("Call outcome saved successfully!")

# =========================
# MAIN APP
# =========================
def main_app():
    st.title("🚗 Motor Renewal CRM")

    st.write(f"Welcome **{st.session_state.username}** ({st.session_state.role})")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

    view_clients()
    update_outcome()

# =========================
# APP FLOW (IMPORTANT FIX HERE)
# =========================
if not st.session_state.logged_in:
    login()
else:
    main_app()
