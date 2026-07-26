import pandas as pd
from datetime import datetime
from supabase_client import supabase


# =====================================
# SAVE CALL RECORD
# =====================================

def save_call_record(
    policy_number,
    policy_holder,
    vehicle_registration,
    premium,
    call_status,
    feedback,
    next_follow_up,
    renewed,
    whatsapp_status,
    username="Milliano"
):

    data = {

        "policy_number": policy_number,

        "policy_holder": policy_holder,

        "vehicle_registration": vehicle_registration,

        "premium": None if pd.isna(premium) else float(premium),

        "call_date": datetime.now().isoformat(),

        "call_status": call_status,

        "feedback": feedback,

        "next_follow_up": str(next_follow_up),

        "renewed": renewed,
        "whatsapp_status": whatsapp_status,

        "username": username

    }

    supabase.table("call_logs").insert(data).execute()


# =====================================
# CLIENT HISTORY
# =====================================

def get_client_history(policy_number):

    response = (
        supabase
        .table("call_logs")
        .select("*")
        .eq("policy_number", policy_number)
        .order("call_date", desc=True)
        .execute()
    )

    return pd.DataFrame(response.data)


# =====================================
# ALL CALL LOGS
# =====================================

def get_all_call_logs():

    response = (
        supabase
        .table("call_logs")
        .select("*")
        .order("call_date", desc=True)
        .execute()
    )

    return pd.DataFrame(response.data)


# =====================================
# TODAY'S CALLS
# =====================================

def get_today_calls():

    today = datetime.now().strftime("%Y-%m-%d")

    response = (
        supabase
        .table("call_logs")
        .select("*")
        .gte("call_date", today)
        .execute()
    )

    return pd.DataFrame(response.data)


# =====================================
# RENEWED CLIENTS
# =====================================

def get_renewed_clients():

    response = (
        supabase
        .table("call_logs")
        .select("*")
        .eq("renewed", "Yes")
        .execute()
    )

    return pd.DataFrame(response.data)


# =====================================
# PENDING FOLLOW UPS
# =====================================

def get_pending_followups():

    response = (
        supabase
        .table("call_logs")
        .select("*")
        .eq("renewed", "No")
        .execute()
    )

    return pd.DataFrame(response.data)
