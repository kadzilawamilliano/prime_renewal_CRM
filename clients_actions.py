
import urllib.parse
import pandas as pd
import streamlit as st

from utils import clean_phone


def client_buttons(row):

    local_phone, wa_phone = clean_phone(
        row["phone_number"]
    )

    renewal_date = pd.to_datetime(
        row["renewal_date"]
    )

    expiry = renewal_date - pd.Timedelta(days=1)

    message = f"""
Hello {row['policy_holder']},

My name is Milliano Kadzilawa from Prime Insurance Company.

This is a reminder that your insurance policy for vehicle
{row['vehicle_reg']}
expires on
{expiry.strftime('%d %B %Y')}.

Kindly renew your policy.

Thank you.
"""

    encoded = urllib.parse.quote(message)

    whatsapp = (
        f"https://wa.me/{wa_phone}?text={encoded}"
    )

    st.link_button(
        "💬 WhatsApp Client",
        whatsapp
    )

    st.markdown(
        f'<a href="tel:{local_phone}">📞 Call Client</a>',
        unsafe_allow_html=True
    )
