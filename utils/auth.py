import streamlit as st

# if not st.experimental_user.is_logged_in:
#     if st.button("Log in with Google"):
#         st.login()
#     st.stop()

# if st.button("Log out"):
#     st.logout()

def login():
    if st.button(":material/login:", type="tertiary", use_container_width=True):
        st.login()
        # st.session_state.authenticated = True

# def is_authenticated():
#     return st.session_state.get("authenticated", False)

def authenticate():
    # if not is_authenticated():
    #     login()
    #     st.stop()
    
    if not st.experimental_user.is_logged_in:
        st.button(
            "Log in with Google", 
            icon=":material/login:", 
            type="tertiary", 
            use_container_width=True, 
            on_click=st.login
        )
        st.stop()

def get_user_info():
    if st.experimental_user.is_logged_in:
        return st.experimental_user

def log_out():
    st.button("Log out", icon=":material/logout:", type="tertiary", on_click=st.logout)