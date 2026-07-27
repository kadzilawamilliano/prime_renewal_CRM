import re
import urllib.parse
import pandas as pd


# =====================================
# FORMAT MALAWI PHONE NUMBER
# =====================================

def format_phone(phone):

    phone = str(phone)

    phone = re.sub(r"\D", "", phone)

    if phone.startswith("265"):

        local_phone = "0" + phone[3:]

    else:

        local_phone = phone

    whatsapp_phone = local_phone

    if whatsapp_phone.startswith("0"):

        whatsapp_phone = "265" + whatsapp_phone[1:]

    return local_phone, whatsapp_phone


# =====================================
# CALCULATE EXPIRY DATE
# =====================================

def get_expiry_date(renewal_date):

    renewal_date = pd.to_datetime(

        renewal_date,

        errors="coerce"

    )

    expiry_date = renewal_date - pd.Timedelta(days=1)

    return expiry_date.strftime("%d %B %Y")


# =====================================
# CREATE WHATSAPP MESSAGE
# =====================================

def whatsapp_message(

    name,

    vehicle,

    expiry_date

):

    return f"""

Hello {name},

My name is Milliano Kadzilawa from Prime Insurance Company Limited.

This is a friendly reminder that your motor insurance policy for vehicle {vehicle} is expected to expire on {expiry_date}.

We kindly encourage you to renew your insurance through our agents or visit our office directly for assistance.

Thank you for trusting Prime Insurance Company.

"""


# =====================================
# CREATE WHATSAPP LINK
# =====================================

def whatsapp_link(

    phone,

    message

):

    encoded = urllib.parse.quote(message)

    return f"https://wa.me/{phone}?text={encoded}"


# =====================================
# CREATE CALL LINK
# =====================================

def call_link(phone):

    return f"tel:{phone}"
