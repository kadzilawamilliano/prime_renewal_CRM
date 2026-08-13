import streamlit as st
import pandas as pd
from supabase_client import supabase


def show(df):

    # =====================================
    # SECTION 3
    # CALL STATUS BREAKDOWN
    # =====================================

    st.divider()

    st.subheader(
        ":material/pie_chart: Call Status Breakdown"
    )

    try:

        # ---------------------------------
        # Fetch ALL call logs
        # ---------------------------------

        all_logs = []

        page_size = 1000
        start = 0

        while True:

            response = (
                supabase
                .table("call_logs")
                .select("call_status")
                .range(
                    start,
                    start + page_size - 1
                )
                .execute()
            )

            batch = response.data

            if not batch:
                break

            all_logs.extend(batch)

            if len(batch) < page_size:
                break

            start += page_size

        # ---------------------------------
        # Convert to DataFrame
        # ---------------------------------

        status_df = pd.DataFrame(all_logs)

        if status_df.empty:

            st.warning(
                "No call status records found."
            )

        else:

            # ---------------------------------
            # Clean call status
            # ---------------------------------

            status_df["call_status"] = (
                status_df["call_status"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

            # ---------------------------------
            # Standardise status names
            # ---------------------------------

            status_df["call_status"] = (
                status_df["call_status"]
                .replace(
                    {
                        "Not reachable": "Not Reachable",
                        "not reachable": "Not Reachable",
                        "NOT REACHABLE": "Not Reachable",

                        "will renew": "Will Renew",
                        "WILL RENEW": "Will Renew",

                        "no answer": "No Answer",
                        "NO ANSWER": "No Answer",

                        "busy": "Busy",
                        "BUSY": "Busy",

                        "wrong number": "Wrong Number",
                        "WRONG NUMBER": "Wrong Number",

                        "pending decision": "Pending Decision",
                        "PENDING DECISION": "Pending Decision"
                    }
                )
            )

            # ---------------------------------
            # Count each call status
            # ---------------------------------

            status_counts = (
                status_df["call_status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Call Status",
                "Number of Calls"
            ]

            # ---------------------------------
            # Display total calls
            # ---------------------------------

            st.info(
                f"Total Call Records Analysed: "
                f"{len(status_df)}"
            )

            # ---------------------------------
            # Display table
            # ---------------------------------

            st.dataframe(
                status_counts,
                use_container_width=True,
                hide_index=True
            )

            # ---------------------------------
            # Display chart
            # ---------------------------------

            chart_data = (
                status_counts
                .set_index("Call Status")
            )

            st.bar_chart(
                chart_data
            )

    except Exception as e:

        st.error(
            f"Error loading call status breakdown: {e}"
        )


    # =====================================
    # SECTION 4
    # FOLLOW-UP PRIORITY LIST
    # =====================================
        # =====================================
    # SECTION 4
    # FOLLOW-UP PRIORITY LIST
    # =====================================

    st.divider()

    st.subheader(
        ":material/priority_high: Follow-Up Priority List"
    )

    try:

        # ---------------------------------
        # DATE FILTERS
        # ---------------------------------

        col1, col2 = st.columns(2)

        with col1:

            follow_from_date = st.date_input(
                "Follow-Up Call Date From",
                key="follow_from_date"
            )

        with col2:

            follow_to_date = st.date_input(
                "Follow-Up Call Date To",
                key="follow_to_date"
            )

        # ---------------------------------
        # VALIDATE DATE RANGE
        # ---------------------------------

        if follow_from_date > follow_to_date:

            st.error(
                "⚠️ 'Call Date From' cannot be later "
                "than 'Call Date To'."
            )

            st.stop()

        # ---------------------------------
        # FULL DAY DATETIME RANGE
        # ---------------------------------

        follow_from_datetime = (
            f"{follow_from_date}T00:00:00"
        )

        follow_to_datetime = (
            f"{follow_to_date}T23:59:59"
        )

        # ---------------------------------
        # FETCH FOLLOW-UP RECORDS
        # ---------------------------------

        all_followups = []

        page_size = 1000
        start = 0

        while True:

            response = (
                supabase
                .table("call_logs")
                .select("*")
                .gte(
                    "call_date",
                    follow_from_datetime
                )
                .lte(
                    "call_date",
                    follow_to_datetime
                )
                .range(
                    start,
                    start + page_size - 1
                )
                .execute()
            )

            batch = response.data

            if not batch:
                break

            all_followups.extend(batch)

            if len(batch) < page_size:
                break

            start += page_size

        # ---------------------------------
        # CONVERT TO DATAFRAME
        # ---------------------------------

        follow_df = pd.DataFrame(
            all_followups
        )

        # ---------------------------------
        # CHECK DATA
        # ---------------------------------

        if follow_df.empty:

            st.info(
                "No call records found for the "
                "selected period."
            )

        else:

            # ---------------------------------
            # CLEAN CALL STATUS
            # ---------------------------------

            follow_df["call_status"] = (
                follow_df["call_status"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

            # ---------------------------------
            # CLEAN WHATSAPP STATUS
            # ---------------------------------

            follow_df["whatsapp_status"] = (
                follow_df["whatsapp_status"]
                .fillna("Not Checked")
                .astype(str)
                .str.strip()
            )

            # ---------------------------------
            # STANDARDISE CALL STATUS
            # ---------------------------------

            follow_df["call_status"] = (
                follow_df["call_status"]
                .replace(
                    {
                        "Not reachable": "Not Reachable",
                        "not reachable": "Not Reachable",
                        "NOT REACHABLE": "Not Reachable",

                        "will renew": "Will Renew",
                        "WILL RENEW": "Will Renew",

                        "no answer": "No Answer",
                        "NO ANSWER": "No Answer",

                        "pending decision": "Pending Decision",
                        "PENDING DECISION": "Pending Decision"
                    }
                )
            )

            # =================================
            # HIGH PRIORITY
            # =================================

            high_priority = follow_df[
                (
                    follow_df["call_status"]
                    == "Not Reachable"
                )
                &
                (
                    follow_df["whatsapp_status"]
                    == "No WhatsApp"
                )
            ].copy()

            high_priority["Priority"] = "HIGH"

            # =================================
            # MEDIUM PRIORITY
            # =================================

            medium_priority = follow_df[
                (
                    (
                        follow_df["call_status"]
                        == "No Answer"
                    )
                    &
                    (
                        follow_df["whatsapp_status"]
                        == "Message Sent"
                    )
                )
                |
                (
                    follow_df["call_status"]
                    == "Pending Decision"
                )
            ].copy()

            medium_priority["Priority"] = "MEDIUM"

            # =================================
            # LOW PRIORITY
            # =================================

            low_priority = follow_df[
                follow_df["call_status"]
                == "Will Renew"
            ].copy()

            low_priority["Priority"] = "LOW"

            # =================================
            # COMBINE PRIORITY LIST
            # =================================

            priority_list = pd.concat(
                [
                    high_priority,
                    medium_priority,
                    low_priority
                ],
                ignore_index=True
            )

            # =================================
            # DISPLAY RESULTS
            # =================================

            if priority_list.empty:

                st.info(
                    "No priority follow-ups found "
                    "for the selected period."
                )

            else:

                # ---------------------------------
                # PRIORITY ORDER
                # ---------------------------------

                priority_order = {
                    "HIGH": 1,
                    "MEDIUM": 2,
                    "LOW": 3
                }

                priority_list["Order"] = (
                    priority_list["Priority"]
                    .map(priority_order)
                )

                priority_list = (
                    priority_list
                    .sort_values("Order")
                    .drop(columns=["Order"])
                )

                # ---------------------------------
                # SUMMARY
                # ---------------------------------

                high_count = len(high_priority)

                medium_count = len(medium_priority)

                low_count = len(low_priority)

                st.info(
                    f"Follow-ups found: "
                    f"{len(priority_list)}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "🔴 High Priority",
                        high_count
                    )

                with col2:

                    st.metric(
                        "🟠 Medium Priority",
                        medium_count
                    )

                with col3:

                    st.metric(
                        "🟢 Low Priority",
                        low_count
                    )

                # ---------------------------------
                # DISPLAY TABLE
                # ---------------------------------

                display_columns = [
                    "policy_number",
                    "policy_holder",
                    "call_date",
                    "call_status",
                    "whatsapp_status",
                    "feedback",
                    "next_follow_up",
                    "Priority"
                ]

                # Only use columns that exist

                display_columns = [
                    column
                    for column in display_columns
                    if column in priority_list.columns
                ]

                st.dataframe(
                    priority_list[
                        display_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                # ---------------------------------
                # DOWNLOAD
                # ---------------------------------

                csv = priority_list.to_csv(
                    index=False
                )

                st.download_button(
                    "📥 Download Follow-Up List",
                    csv,
                    file_name=(
                        f"follow_up_"
                        f"{follow_from_date}_"
                        f"to_{follow_to_date}.csv"
                    ),
                    mime="text/csv"
                )

    except Exception as e:

        st.error(
            f"Error loading follow-up list: {e}"
                )
