import streamlit as st
import pandas as pd
from supabase_client import supabase


def show(df):

    st.title(":material/analytics: Reports")

    st.divider()

    st.subheader(":material/call: Call Performance")

    try:

        response = (
            supabase
            .table("call_logs")
            .select("*")
            .execute()
        )

        logs = pd.DataFrame(response.data)

        if logs.empty:

            st.warning("No call records found.")

        else:

            # Convert call_date to datetime
            logs["call_date"] = pd.to_datetime(
                logs["call_date"],
                errors="coerce"
            )

            # Current date
            today = pd.Timestamp.now().normalize()

            # Total calls
            total_calls = len(logs)

            # Calls today
            calls_today = (
                logs["call_date"].dt.normalize() == today
            ).sum()

            # Calls this week
            start_of_week = today - pd.Timedelta(days=today.weekday())

            calls_this_week = (
                logs["call_date"] >= start_of_week
            ).sum()

            # Calls this month
            start_of_month = today.replace(day=1)

            calls_this_month = (
                logs["call_date"] >= start_of_month
            ).sum()

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Calls",
                    total_calls
                )

            with col2:
                st.metric(
                    "Calls Today",
                    calls_today
                )

            with col3:
                st.metric(
                    "Calls This Week",

            # =====================================
    # CALL STATUS BREAKDOWN
    # =====================================

    st.divider()

    st.subheader(":material/pie_chart: Call Status Breakdown")

    try:

        response = (
            supabase
            .table("call_logs")
            .select("call_status")
            .execute()
        )

        status_df = pd.DataFrame(response.data)

        if status_df.empty:

            st.warning("No call status records found.")

        else:

            # Clean call status values
            status_df["call_status"] = (
                status_df["call_status"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

            # Count each call status
            status_counts = (
                status_df["call_status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Call Status",
                "Number of Calls"
            ]

            # Display summary table
            st.dataframe(
                status_counts,
                use_container_width=True
            )


            # Display chart
            st.bar_chart(
                status_counts.set_index(
                    "Call Status"
                )
            )


    except Exception as e:

        st.error(
            f"Error loading call status breakdown: {e}"
        )
            # =====================================
    # FOLLOW-UP PRIORITY LIST
    # =====================================

    st.divider()

    st.subheader(":material/priority_high: Follow-Up Priority List")


    try:

        response = (
            supabase
            .table("call_logs")
            .select("*")
            .execute()
        )


        follow_df = pd.DataFrame(response.data)


        if follow_df.empty:

            st.warning(
                "No follow-up records found."
            )

        else:


            # Clean data

            follow_df["call_status"] = (
                follow_df["call_status"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )


            follow_df["whatsapp_status"] = (
                follow_df["whatsapp_status"]
                .fillna("Not Checked")
                .astype(str)
                .str.strip()
            )


            # ==============================
            # HIGH PRIORITY
            # ==============================

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



            # ==============================
            # MEDIUM PRIORITY
            # ==============================

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



            # ==============================
            # LOW PRIORITY
            # ==============================

            low_priority = follow_df[
                follow_df["call_status"]
                == "Will Renew"
            ].copy()


            low_priority["Priority"] = "LOW"



            # Combine all follow-ups

            priority_list = pd.concat(
                [
                    high_priority,
                    medium_priority,
                    low_priority
                ],
                ignore_index=True
            )


            if priority_list.empty:

                st.info(
                    "No follow-up customers available."
                )

            else:


                # Arrange HIGH first

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


                st.dataframe(
                    priority_list[
                        [
                            "policy_number",
                            "policy_holder",
                            "call_status",
                            "whatsapp_status",
                            "feedback",
                            "next_follow_up",
                            "Priority"
                        ]
                    ],
                    use_container_width=True
                )


                # Download CSV

                csv = priority_list.to_csv(
                    index=False
                )


                st.download_button(
                    "📥 Download Follow-Up List",
                    csv,
                    file_name="follow_up_priority_list.csv",
                    mime="text/csv"
                )


    except Exception as e:

        st.error(
            f"Error loading follow-up list: {e}"
                )
