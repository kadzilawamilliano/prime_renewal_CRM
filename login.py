import streamlit as st
from supabase_client import supabase


def login():

    st.title("🔐 Motor Renewal CRM")

    st.subheader("Sign in to continue")

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        try:

            response = (
                supabase.auth.sign_in_with_password(
                    {
                        "email": email,
                        "password": password
                    }
                )
            )

            if response.user:

                st.session_state["logged_in"] = True

                st.session_state["user"] = response.user.email

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

        except Exception as e:

            st.error(
                f"Login failed: {e}"
            )
