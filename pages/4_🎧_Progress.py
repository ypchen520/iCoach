import streamlit as st
from st_circular_progress import CircularProgress
import base64
import math
# import pendulum
# import time
from utils import sprite, utils, clock, auth

st.set_page_config(layout="wide")

# Function to calculate level based on experience
def calculate_level(exp):
    # Simple level formula: level = sqrt(exp / 100)
    return math.floor(math.sqrt(exp / 100)) + 1

# Function to calculate experience percentage to next level
def calculate_exp_percentage(exp):
    current_level = calculate_level(exp)
    exp_needed_for_current = 100 * (current_level - 1) ** 2
    exp_needed_for_next = 100 * current_level ** 2
    
    exp_in_current_level = exp - exp_needed_for_current
    exp_to_next_level = exp_needed_for_next - exp_needed_for_current
    
    return min(100, (exp_in_current_level / exp_to_next_level) * 100)

auth.authenticate()

sprite_sheet_path = "assets/Knights/Troops/Warrior/Purple/Warrior_Purple.png"

total_exp = 50

# Calculate level and experience percentage
level = calculate_level(total_exp)
exp_percentage = calculate_exp_percentage(total_exp)

# Calculate "life"
num_prev_todo = 7
num_prev_done = 3
curr_life = 100 # pull from firestore

life_percentage = min(100, int(curr_life - (1-(num_prev_done / num_prev_todo)) * 100))


# Display character with circular progress bars
sprite.display_character_with_progress(
    sprite_sheet_path, 
    exp_percentage,
    life_percentage,
    level
)

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