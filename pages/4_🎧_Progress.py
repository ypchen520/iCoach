import streamlit as st
from st_circular_progress import CircularProgress
import base64
import pendulum
import time

# tabs: daily, weekly, monthly
daily_tab, weekly_tab, monthly_tab = st.tabs([":sunny: Daily", ":calendar: Weekly", ":full_moon: Monthly"])

# daily_minute_goal = 330
# daily_accumulated_minutes = 17 # pull data from fb

# Set background image
def set_bg_hack(main_bg):
    """
    A function to set the background image of the app.
    """
    main_bg_ext = main_bg.split(".")[-1]

    b64_main_bg = base64.b64encode(open(main_bg, "rb").read()).decode("utf-8")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{main_bg_ext};base64,{b64_main_bg}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load and display image
image_path = "images/high-above.jpeg" 
set_bg_hack(image_path)

with daily_tab:
    daily_minute_goal = st.number_input(":trophy: Daily minute goal: ", value=300)
    daily_accumulated_minutes = st.number_input(":mechanical_arm: Daily accumulated minutes: ", value=0)
    # st.markdown("<style>h2{}</style>", unsafe_allow_html=True)
    st.markdown("<style>div.block-container{text-align: center;}</style>", unsafe_allow_html=True)
    # st.write(f":trophy: Daily minute goal: {daily_minute_goal}")
    # st.write(f":mechanical_arm: Daily accumulated minutes: {daily_accumulated_minutes}")

    st.write("###")

    progress_percentage = int(daily_accumulated_minutes / daily_minute_goal * 100)

    if progress_percentage < 100:
        text = f":fist: Keep it up, you can do this! {progress_percentage}%"
    else:
        text = ":star: Another day, another win!"
        progress_percentage = 100

    st.progress(progress_percentage, text)

    # def calculate_progress():
    #     if "slider" in st.session_state:
    #         cp.update_value(progress=st.session_state["slider"])

    # columns = st.columns((1, 2))
    # with columns[0]:
    #     cp = CircularProgress(
    #         value=0,
    #         label="Progress Indicator",
    #         size="Large",
    #         key="circular_progress_total",
    #     )
    #     cp.st_circular_progress()
    # with columns[1]:
    #     st.slider(
    #         "Change progress to",
    #         min_value=0,
    #         max_value=100,
    #         on_change=calculate_progress,
    #         key="slider",
    #     )
    # my_circular_progress = CircularProgress(label=text, value=progress_percentage, key="my_circular_progress")
    # my_circular_progress.st_circular_progress()
    # my_circular_progress.update_value(progress=progress_percentage)

    # clock

    clock_container = st.empty()

    while True:
        now = pendulum.now()
        current_time = now.to_time_string()
        clock = f'<span style="color: Black; font-size: 100px;">{current_time}<span>'
        # st.markdown(clock, unsafe_allow_html=True)
        clock_container.write(clock, unsafe_allow_html=True)
        time.sleep(1)