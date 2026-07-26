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
