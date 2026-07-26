import streamlit as st
import pandas as pd
from supabase_client import supabase


def show(df):

    st.title(":material/analytics: Reports")

    st.divider()

    st.subheader(":material/assessment: Portfolio Summary")

    # Ensure Premium is numeric
    df["Premium"] = pd.to_numeric(
        df["Premium"],
        errors="coerce"
    ).fillna(0)

    # Total policies
    total_policies = len(df)

    # Total portfolio premium
    total_premium = df["Premium"].sum()

    # Average premium
    average_premium = df["Premium"].mean()

    # Renewed policies
    renewed = (
        df["Renewed"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
    ).sum()

    # Pending / Not renewed
    pending = (
        df["Renewed"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("no")
    ).sum()

    # Display metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Policies", total_policies)

    with col2:
        st.metric(
            "Portfolio Premium",
            f"MK {total_premium:,.2f}"
        )

    with col3:
        st.metric(
            "Average Premium",
            f"MK {average_premium:,.2f}"
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Renewed Policies", renewed)

    with col5:
        st.metric("Not Renewed", pending)
            # =====================================
    # CALL PERFORMANCE
    # =====================================

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
                    calls_this_week
                )

            with col4:
                st.metric(
                    "Calls This Month",
                    calls_this_month
                )

    except Exception as e:

        st.error(f"Error loading call performance: {e}")
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
