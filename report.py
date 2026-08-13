import streamlit as st
import pandas as pd
from supabase_client import supabase


def show(df):

        # =====================================
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
