from clients_actions import client_buttons
import pandas as pd
import streamlit as st

# Load your clients
clients = pd.read_excel("motor_renewals_tracking.xlsx")

# Display buttons for each client
for index, row in clients.iterrows():

    st.write(row["policy_holder"])
    st.write(row["vehicle_reg"])

    client_buttons(row)
