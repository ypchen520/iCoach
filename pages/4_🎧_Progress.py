import streamlit as st
from st_circular_progress import CircularProgress
import base64
# import pendulum
# import time
from utils import sprite, utils, clock, auth

auth.authenticate()

sprite.add_character_sprite("assets/Knights/Troops/Warrior/Purple/Warrior_Purple.png", position="bottom-right")

# tabs: daily, weekly, monthly
daily_tab, weekly_tab, monthly_tab = st.tabs([":sunny: Daily", ":calendar: Weekly", ":full_moon: Monthly"])

# daily_minute_goal = 330
# daily_accumulated_minutes = 17 # pull data from fb

if "daily_minute_goal" not in st.session_state:
    st.session_state.daily_minute_goal = 300

if 'daily_accumulated_minutes' not in st.session_state:
    # [TODO]: this should eventually be from the db, a doc that keeps track of all task minutes, I pull that doc for today, and sum up the minutes
    st.session_state.daily_accumulated_minutes = 0

# Set background image


# Load and display image
image_path = "assets/high-above.jpeg" 
utils.set_bg(image_path)

with daily_tab:
    st.session_state.daily_minute_goal = st.number_input(":trophy: Daily minute goal: ", value=st.session_state.daily_minute_goal)
    st.session_state.daily_accumulated_minutes = st.number_input(":mechanical_arm: Daily accumulated minutes: ", value=st.session_state.daily_accumulated_minutes)
    # st.markdown("<style>h2{}</style>", unsafe_allow_html=True)
    st.markdown("<style>div.block-container{text-align: center;}</style>", unsafe_allow_html=True)
    # st.write(f":trophy: Daily minute goal: {daily_minute_goal}")
    # st.write(f":mechanical_arm: Daily accumulated minutes: {daily_accumulated_minutes}")

    st.write("###")

    progress_percentage = int(st.session_state.daily_accumulated_minutes / st.session_state.daily_minute_goal * 100)

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

    clock.clock()

    # clock_container = st.empty()

    # while True:
    #     now = pendulum.now()
    #     current_time = now.to_time_string()
    #     clock = f'<span style="color: Black; font-size: 100px;">{current_time}<span>'
    #     # st.markdown(clock, unsafe_allow_html=True)
    #     clock_container.write(clock, unsafe_allow_html=True)
    #     time.sleep(1)