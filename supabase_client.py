from supabase import create_client, Client
import streamlit as st

SUPABASE_URL = "https://hswjymbopblwzmwbhmxk.supabase.co"
SUPABASE_KEY = "sb_publishable_X0nGEGiieiPklP67_A-xEQ_NENBgLHG"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
