import streamlit as st
import pandas as pd

from utils.database import save_whatsapp_reminder

from utils.whatsapp import (
    format_phone,
    get_expiry_date,
    whatsapp_message,
    whatsapp_link
)


def show_whatsapp_reminders(df):

    st.header(":material/chat: WhatsApp Reminders")


    # -----------------------------------
    # Prepare Dates
    # -----------------------------------

    today = pd.Timestamp.today().normalize()

    df = df.copy()

    df["Renewal Date"] = pd.to_datetime(
        df["Renewal Date"],
        errors="coerce"
    )


    # -----------------------------------
    # Filters
    # -----------------------------------

    col1, col2 = st.columns(2)


    with col1:

        filter_option = st.selectbox(
            "Reminder Period",
            [
                "Today",
                "Tomorrow",
                "Next 7 Days",
                "All"
            ]
        )


    with col2:

        if "Branch" in df.columns:

            branches = ["All"] + sorted(
                df["Branch"]
                .dropna()
                .unique()
                .tolist()
            )

            branch = st.selectbox(
                "Branch",
                branches
            )

        else:

            branch = "All"



    # -----------------------------------
    # Date Filter
    # -----------------------------------

    if filter_option == "Today":

        reminders = df[
            df["Renewal Date"]
            .dt.normalize()
            == today
        ]


    elif filter_option == "Tomorrow":

        reminders = df[
            df["Renewal Date"]
            .dt.normalize()
            ==
            today + pd.Timedelta(days=1)
        ]


    elif filter_option == "Next 7 Days":

        reminders = df[
            (
                df["Renewal Date"]
                .dt.normalize()
                >= today
            )
            &
            (
                df["Renewal Date"]
                .dt.normalize()
                <= today + pd.Timedelta(days=7)
            )
        ]


    else:

        reminders = df.copy()



    # -----------------------------------
    # Branch Filter
    # -----------------------------------

    if branch != "All":

        reminders = reminders[
            reminders["Branch"] == branch
        ]


    reminders = reminders.reset_index(drop=True)



    # -----------------------------------
    # No Clients
    # -----------------------------------

    if reminders.empty:

        st.success(
            "🎉 No reminders found."
        )

        return



    # -----------------------------------
    # Session State
    # -----------------------------------

    if "current_whatsapp_client" not in st.session_state:

        st.session_state.current_whatsapp_client = 0



    if (
        st.session_state.current_whatsapp_client
        >= len(reminders)
    ):

        st.session_state.current_whatsapp_client = 0



    # -----------------------------------
    # Select Starting Client
    # -----------------------------------

    start_client = st.selectbox(

        "Start From Client",

        range(
            1,
            len(reminders) + 1
        ),

        index=st.session_state.current_whatsapp_client

    )


    if (
        start_client - 1
        != st.session_state.current_whatsapp_client
    ):

        st.session_state.current_whatsapp_client = start_client - 1

        st.rerun()



    index = st.session_state.current_whatsapp_client


    client = reminders.iloc[index]



    # -----------------------------------
    # Progress
    # -----------------------------------

    st.info(
        f"Client {index + 1} of {len(reminders)}"
    )


    st.divider()



    # -----------------------------------
    # Client Information
    # -----------------------------------

    st.subheader(
        client["Policy Holder"]
    )


    left, right = st.columns(2)


    with left:

        st.write(
            f"🚗 Vehicle: {client['Vehicle Registration']}"
        )


        st.write(
            f"📄 Policy Number: {client['Policy Number']}"
        )


        st.write(
            f"📞 Phone: {client['Phone Number']}"
        )



    with right:

        st.write(
            f"📅 Renewal Date: "
            f"{client['Renewal Date'].strftime('%d %B %Y')}"
        )


        st.write(
            f"💰 Premium: {client['Premium']}"
        )



    st.divider()



    # -----------------------------------
    # WhatsApp
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


    st.link_button(

        ":material/chat: Open WhatsApp",

        whatsapp_url,

        use_container_width=True

    )



    st.divider()



    # -----------------------------------
    # Mark as Sent
    # -----------------------------------

    if st.button(

        "✅ Mark as Sent",

        use_container_width=True

    ):


        save_whatsapp_reminder(

            policy_number=client["Policy Number"],

            policy_holder=client["Policy Holder"],

            vehicle_registration=client["Vehicle Registration"],

            premium=client["Premium"]

        )


        st.success(

            "WhatsApp reminder saved."

        )


        if index < len(reminders) - 1:

            st.session_state.current_whatsapp_client += 1


        else:

            st.session_state.current_whatsapp_client = 0


        st.rerun()



    st.divider()



    # -----------------------------------
    # Navigation
    # -----------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if st.button(

            "⬅ Previous",

            use_container_width=True

        ):


            if index > 0:

                st.session_state.current_whatsapp_client -= 1

                st.rerun()



    with col2:

        if st.button(

            "Next ➡",

            use_container_width=True

        ):


            if index < len(reminders) - 1:

                st.session_state.current_whatsapp_client += 1

                st.rerun()
