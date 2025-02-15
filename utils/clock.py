import streamlit as st
import pendulum

@st.fragment(run_every="1s")
def clock():
    clock_container = st.empty()

    now = pendulum.now()
    current_time = now.to_time_string()
    clock = f'<span style="color: Black; font-size: 100px;">{current_time}<span>'
    # st.markdown(clock, unsafe_allow_html=True)
    clock_container.write(clock, unsafe_allow_html=True)
    # time.sleep(1)