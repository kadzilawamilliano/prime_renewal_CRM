import streamlit as st
import pandas as pd
from supabase_client import supabase


def show(df):

    st.title(":material/analytics: Reports")

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
