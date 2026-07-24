from supabase import create_client, Client
import streamlit as st

SUPABASE_URL = st.secrets["youhswjymbopblwzmwbhmxk"]
SUPABASE_KEY = st.secrets["sb_publishable_X0nGEGiieiPklP67_A-xEQ_NENBgLHG"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
