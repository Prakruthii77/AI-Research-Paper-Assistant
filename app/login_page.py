import streamlit as st

VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

def login_page():
    st.title("🔐 Login to AI Research Paper Assistant")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password!")

    return st.session_state.logged_in