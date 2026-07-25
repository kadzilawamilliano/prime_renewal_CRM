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
