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

    # -----------------------------------
    # SEARCH
    # -----------------------------------

    search = st.text_input(
        "🔍 Search Client or Vehicle Registration"
    )

    # -----------------------------------
    # DATE FILTER
    # -----------------------------------

    today = pd.Timestamp.today().normalize()

    df = df.copy()

    df["Renewal Date"] = pd.to_datetime(
        df["Renewal Date"],
        errors="coerce"
    )

    period = st.selectbox(
        "Reminder Period",
        [
            "All",
            "Today",
            "Tomorrow",
            "Next 7 Days",
            
        ]
    )

    if period == "Today":

        queue = df[
            df["Renewal Date"].dt.normalize()
            == today
        ]

    elif period == "Tomorrow":

        queue = df[
            df["Renewal Date"].dt.normalize()
            ==
            today + pd.Timedelta(days=1)
        ]

    elif period == "Next 7 Days":

        queue = df[
            (
                df["Renewal Date"].dt.normalize()
                >= today
            )
            &
            (
                df["Renewal Date"].dt.normalize()
                <= today + pd.Timedelta(days=7)
            )
        ]

    else:

        queue = df.copy()

    queue = queue.reset_index(drop=True)

    # -----------------------------------
    # SEARCH MODE
    # -----------------------------------

    if search:

        queue = queue[
            queue.astype(str)
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

    if queue.empty:

        st.warning(
            "No client found."
        )

        return

    # -----------------------------------
    # SESSION STATE
    # -----------------------------------

    if "current_client" not in st.session_state:

        st.session_state.current_client = 0

    if (
        st.session_state.current_client
        >= len(queue)
    ):

        st.session_state.current_client = 0

    # -----------------------------------
    # START FROM CLIENT
    # -----------------------------------

    start = st.selectbox(

        "Start From Client",

        range(
            1,
            len(queue) + 1
        ),

        index=st.session_state.current_client

    )

    if (
        start - 1
        != st.session_state.current_client
    ):

        st.session_state.current_client = start - 1

        st.rerun()

    index = st.session_state.current_client

    client = queue.iloc[index]

    # -----------------------------------
    # CLIENT SUMMARY
    # -----------------------------------

    st.divider()

    st.info(
        f"Client {index + 1} of {len(queue)}"
    )

    st.subheader(
        client["Policy Holder"]
    )

    left, right = st.columns(2)

    with left:

        st.write(
            f"🚗 **Vehicle:** {client['Vehicle Registration']}"
        )

        st.write(
            f"📄 **Policy:** {client['Policy Number']}"
        )

        st.write(
            f"📞 **Phone:** {client['Phone Number']}"
        )

    with right:

        st.write(
            f"📅 **Renewal:** "
            f"{client['Renewal Date'].strftime('%d %B %Y')}"
        )

        st.write(
            f"💰 **Premium:** {client['Premium']}"
        )

    # -----------------------------------
    # ACTION BUTTONS
    # -----------------------------------

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
            call_url,
            use_container_width=True
        )

    with c2:

        st.link_button(
            ":material/chat: WhatsApp",
            whatsapp_url,
            use_container_width=True
        )

    st.divider()

    
        # -----------------------------------
    # CALL OUTCOME
    # -----------------------------------

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

    # -----------------------------------
    # SMART DEFAULTS
    # -----------------------------------

    default_renewed = "No"
    default_whatsapp = "Not Checked"

    if call_status == "Renewed Already":

        default_renewed = "Yes"
        default_whatsapp = "Message Sent"

    elif call_status == "Wrong Number":

        default_whatsapp = "No WhatsApp"

    elif call_status == "Invalid Number":

        default_whatsapp = "Failed"

    feedback = st.text_area(
        "Feedback"
    )

    follow_up = st.date_input(
        "Next Follow Up",
        datetime.today()
    )

    renewed = st.selectbox(

        "Renewed",

        ["No", "Yes"],

        index=0 if default_renewed == "No" else 1

    )

    whatsapp_options = [

        "Not Checked",

        "Message Sent",

        "No WhatsApp",

        "Failed"

    ]

    whatsapp_status = st.selectbox(

        "WhatsApp Status",

        whatsapp_options,

        index=whatsapp_options.index(default_whatsapp)

    )

    st.divider()

    if st.button(

        ":material/save: Save & Next Client",

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

            renewed=renewed,

            whatsapp_status=whatsapp_status

        )

        st.success(
            "Call record saved successfully."
        )

        if st.session_state.current_client < len(queue) - 1:

            st.session_state.current_client += 1

        else:

            st.session_state.current_client = 0

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
                    f"📅 {row['call_date']}"
                )

                st.write(
                    f"Status: {row['call_status']}"
                )

                st.write(
                    f"Feedback: {row['feedback']}"
                )

                st.write(
                    f"Next Follow Up: {row['next_follow_up']}"
                )

                st.write(
                    f"Renewed: {row['renewed']}"
                )

                st.write(
                    f"WhatsApp: {row['whatsapp_status']}"
                )


    
