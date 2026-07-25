import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import (
    save_call_record,
    get_client_history
)

from utils.whatsapp import (
    format_phone,
    get_expiry_date,
    whatsapp_message,
    whatsapp_link,
    call_link
)
def show_client_management(df):
    st.header(":material/groups: Client Management")

    search = st.text_input(
        "Search Client"
    )

    if search:

        filtered = df[

            df.astype(str)

            .apply(

                lambda x:

                x.str.contains(

                    search,

                    case=False,

                    na=False

                ).any(),

                axis=1

            )

        ]

    else:

        filtered = df

    if filtered.empty:

        st.warning("Client not found.")

        return

    client = st.selectbox(

        "Select Client",

        filtered["Policy Holder"]

        .dropna()

        .unique()

    )

    client = filtered[

        filtered["Policy Holder"] == client

    ].iloc[0]
    st.divider()

    st.subheader(":material/person: Client Profile")

    left, right = st.columns(2)

    with left:

        st.info(client["Policy Number"])

        st.info(client["Policy Holder"])

        st.info(client["Vehicle Registration"])

    with right:

        st.info(client["Premium"])

        st.info(client["Commencement Date"])

        st.info(client["Renewal Date"])

            local_phone, whatsapp_phone = format_phone(

        client["Phone Number"]

    )

    expiry = get_expiry_date(

        client["Renewal Date"]

    )

    message = whatsapp_message(

        client["Policy Holder"],

        client["Vehicle Registration"],

        expiry

    )

    whatsapp_url = whatsapp_link(

        whatsapp_phone,

        message

    )

    call_url = call_link(

        local_phone

    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.link_button(

            ":material/call: Call Client",

            call_url

        )

    with c2:

        st.link_button(

            ":material/chat: WhatsApp",

            whatsapp_url

        )
    st.divider()

    st.subheader(

        ":material/edit_note: Call Outcome"

    )

    call_status = st.selectbox(

        "Call Status",

        [

            "No Answer",

            "Busy",

            "Wrong Number",

            "Will Renew",

            "Pending Decision",

            "Not Interested",

            "Renewed Already",

            "Not Reachable",

            "Will Not Renew",

            "Invalid Number"

        ]

    )

    feedback = st.text_area(

        "Feedback"

    )

    follow_up = st.date_input(

        "Next Follow Up",

        datetime.today()

    )

    renewed = st.selectbox(

        "Renewed",

        [

            "No",

            "Yes"

        ]

    )
    if st.button(

        ":material/save: Save Record",

        use_container_width=True

    ):

        save_call_record(

            policy_number=client["Policy Number"],

            policy_holder=client["Policy Holder"],

            vehicle_registration=client["Vehicle Registration"],

            premium=client["Premium"],

            call_status=call_status,

            feedback=feedback,

            next_follow_up=follow_up,

            renewed=renewed

        )

        st.success(

            "Call record saved successfully."

        )

        st.rerun()
            st.divider()

    st.subheader(

        ":material/history: Client Timeline"

    )

    history = get_client_history(

        client["Policy Number"]

    )

    if history.empty:

        st.info(

            "No activities yet."

        )

    else:

        for _, row in history.iterrows():

            with st.container(border=True):

                st.write(

                    row["call_date"]

                )

                st.write(

                    row["call_status"]

                )

                st.write(

                    row["feedback"]

                )

                st.write(

                    row["next_follow_up"]

                )

                st.write(

                    row["renewed"]

                )
