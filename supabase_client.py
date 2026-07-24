from supabase import create_client, Client

SUPABASE_URL = "hswjymbopblwzmwbhmxk"
SUPABASE_KEY = "sb_publishable_X0nGEGiieiPklP67_A-xEQ_NENBgLHG"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
