from clients_actions import client_buttons
import pandas as pd
import streamlit as st

# Load your clients
clients = pd.read_excel("motor_renewals_tracking.xlsx")

# Display buttons for each client
for index, row in clients.iterrows():

    st.write(row["Policy Holder"])
    st.write(row["Vehicle Registration"])

    client_buttons(row)
