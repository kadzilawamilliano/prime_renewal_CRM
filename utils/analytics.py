import pandas as pd
from datetime import datetime, timedelta


# =====================================
# KPI SUMMARY
# =====================================

def calculate_kpis(client_data, call_logs):

    total_clients = len(client_data)

    total_calls = len(call_logs)

    renewed_clients = len(
        call_logs[
            call_logs["renewed"] == "Yes"
        ]
    )

    pending_followups = len(
        call_logs[
            call_logs["renewed"] == "No"
        ]
    )

    portfolio_premium = (
        client_data["Premium"]
        .fillna(0)
        .sum()
    )

    retained_premium = (
        call_logs.loc[
            call_logs["renewed"] == "Yes",
            "premium"
        ]
        .fillna(0)
        .sum()
    )

    retention_rate = 0

    if total_clients > 0:

        retention_rate = round(
            (renewed_clients / total_clients) * 100,
            2
        )

    return {

        "total_clients": total_clients,

        "total_calls": total_calls,

        "renewed_clients": renewed_clients,

        "pending_followups": pending_followups,

        "portfolio_premium": portfolio_premium,

        "retained_premium": retained_premium,

        "retention_rate": retention_rate

    }


# =====================================
# DAILY CALLS
# =====================================

def daily_calls(call_logs):

    if call_logs.empty:
        return 0

    logs = call_logs.copy()

    logs["call_date"] = pd.to_datetime(
        logs["call_date"],
        errors="coerce"
    )

    today = datetime.today().date()

    return len(

        logs[
            logs["call_date"].dt.date == today
        ]

    )


# =====================================
# WEEKLY CALLS
# =====================================

def weekly_calls(call_logs):

    if call_logs.empty:
        return 0

    logs = call_logs.copy()

    logs["call_date"] = pd.to_datetime(
        logs["call_date"],
        errors="coerce"
    )

    start = datetime.today() - timedelta(days=7)

    return len(

        logs[
            logs["call_date"] >= start
        ]

    )


# =====================================
# MONTHLY CALLS
# =====================================

def monthly_calls(call_logs):

    if call_logs.empty:
        return 0

    logs = call_logs.copy()

    logs["call_date"] = pd.to_datetime(
        logs["call_date"],
        errors="coerce"
    )

    today = datetime.today()

    return len(

        logs[

            (logs["call_date"].dt.month == today.month)

            &

            (logs["call_date"].dt.year == today.year)

        ]

    )


# =====================================
# CALL STATUS SUMMARY
# =====================================

def call_status_summary(call_logs):

    if call_logs.empty:

        return pd.DataFrame()

    return (

        call_logs["call_status"]

        .value_counts()

        .reset_index()

        .rename(

            columns={

                "index": "Call Status",

                "call_status": "Count"

            }

        )

    )


# =====================================
# OFFICER PERFORMANCE
# =====================================

def officer_performance(call_logs):

    if call_logs.empty:

        return pd.DataFrame()

    return (

        call_logs

        .groupby("username")

        .size()

        .reset_index(name="Calls Made")

        .sort_values(

            by="Calls Made",

            ascending=False

        )

    )


# =====================================
# RECENT ACTIVITIES
# =====================================

def recent_activities(call_logs, limit=10):

    if call_logs.empty:

        return pd.DataFrame()

    logs = call_logs.copy()

    logs["call_date"] = pd.to_datetime(

        logs["call_date"],

        errors="coerce"

    )

    return logs.sort_values(

        by="call_date",

        ascending=False

    ).head(limit)
