import sqlite3

conn = sqlite3.connect("crm.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS clients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
policy_number TEXT,
vehicle_reg TEXT,
premium TEXT,
phone_number TEXT,
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
