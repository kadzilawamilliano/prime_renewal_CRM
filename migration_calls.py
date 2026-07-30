import pandas as pd
from supabase_client import supabase


def migrate_calls():

    EXCEL_FILE = "motor_renewals_tracking.xlsx"

    # ==============================
    # LOAD EXCEL
    # ==============================

    df = pd.read_excel(EXCEL_FILE)

    df.columns = df.columns.str.strip()

    df = df[df["Call Date"].notna()]

    uploaded = 0
    skipped = 0

    for _, row in df.iterrows():

        policy_number = str(
            row["Policy Number"]
        ).strip()

        call_date = pd.to_datetime(
            row["Call Date"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        # ==========================
        # CHECK DUPLICATE
        # ==========================

        existing = (
            supabase
            .table("call_logs")
            .select("id")
            .eq(
                "policy_number",
                policy_number
            )
            .eq(
                "call_date",
                call_date
            )
            .execute()
        )

        if existing.data:

            skipped += 1
            continue

        # ==========================
        # CREATE RECORD
        # ==========================

        record = {

            "policy_number": policy_number,

            "policy_holder": row.get(
                "Policy Holder"
            ),

            "vehicle_registration": row.get(
                "Vehicle Registration"
            ),

            "premium": row.get(
                "Premium",
                None
            ),

            "call_date": call_date,

            "call_status": row.get(
                "Call Status"
            ),

            "feedback": row.get(
                "Feedback"
            ),

            "next_follow_up": row.get(
                "Next Follow Up",
                None
            ),

            "renewed": str(
                row.get(
                    "Renewed",
                    ""
                )
            ),

            "username": "migration",

            "whatsapp_status": row.get(
                "WhatsApp Status",
                "Not Checked"
            )

        }

        # Remove NaN values

        record = {
            k: None if pd.isna(v) else v
            for k, v in record.items()
        }

        # ==========================
        # INSERT
        # ==========================

        supabase.table(
            "call_logs"
        ).insert(
            record
        ).execute()

        uploaded += 1

    return uploaded, skipped
