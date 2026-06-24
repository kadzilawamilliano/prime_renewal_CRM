
%%writefile app.py
import streamlit as st
import pandas as pd

# =============================
# LOAD DATA
# =============================
df = pd.read_excel("/content/drive/MyDrive/Renewals/motor_renewals_tracking.xlsx")

st.set_page_config(page_title="Motor Renewal CRM", layout="wide")

st.title("🚗 Motor Renewal Retention CRM System")
st.caption("Built by Milliano Benjamin kadzilawa")

# =============================
# SESSION STORAGE (CALL LOGS)
# =============================
if "call_logs" not in st.session_state:
    st.session_state.call_logs = {}

# =============================
# STEP 1: SELECT CLIENT
# =============================
# =============================
# STEP 1: SEARCH & SELECT CLIENT
# =============================

search = st.text_input(
    "🔍 Search Client (Name / Policy / Vehicle)"
)

if search:
    filtered_df = df[
        df.astype(str)
        .apply(lambda x: x.str.contains(search, case=False, na=False))
        .any(axis=1)
    ]
else:
    filtered_df = df

client = st.selectbox(
"Select Client",
    filtered_df["Policy Holder"].unique()
)


row = filtered_df[filtered_df["Policy Holder"] == client].iloc[0]

# =============================
# STEP 2: SHOW DETAILS
st.subheader("📄 Client Details")


‎


‎st.write(f"📄 Policy Number: {row['Policy Number']}")


‎st.write(f"📄 Policy Holder: {row['Policy Holder']}")


‎st.write(f"🚘 Vehicle: {row['Vehicle Registration']}")


‎st.write(f"📞 Phone: {row['Phone Number']}")


‎st.write(f"📅 Renewal Date: {row['Renewal Date']}")



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

‎import pandas as pd

‎

‎phone = str(row["Phone Number"]).strip()

‎reg_number = row["Vehicle Registration"]

‎Name = row["Policy Holder"]

import re

phone = str(row["Phone Number"])
phone = re.sub(r"\D", "", phone)  # Remove spaces and other non-digit characters

# Convert international format (265...) to local format (0...)
if phone.startswith("265"):
    phone = "0" + phone[3:]

‎st.markdown(
  f"📞 [Call Client](tel:{phone})",
     unsafe_allow_html=True
    )

‎# Convert renewal date to datetime

‎renewal_date = pd.to_datetime(row["Renewal Date"])

‎

‎# Compute expiry date (1 day before renewal)

‎expiry_date = renewal_date - pd.Timedelta(days=1)

‎

‎# Format date nicely

‎expiry_date_str = expiry_date.strftime("%d %B %Y")



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


!pip install streamlit pyngrok pandas

!streamlit run app.py &>/content/logs.txt &
!ps -ef | grep streamlit

from pyngrok import ngrok

ngrok.set_auth_token("3FKJnE35wKnpzSpEsoFYfly7UVR_2fxoFF4AhNzYRtWSf8nU9")


from pyngrok import ngrok

public_url = ngrok.connect(8501)
print(public_url)


file_path = "/content/app.py"

with open(file_path, "rb") as f:
    data = f.read()

# Remove common hidden Unicode marks
for bad in [
    b'\xe2\x80\x8e',  # U+200E
    b'\xe2\x80\x8f',  # U+200F
    b'\xef\xbb\xbf'   # BOM
]:
    data = data.replace(bad, b'')

with open(file_path, "wb") as f:
    f.write(data)

print("File cleaned successfully.")
