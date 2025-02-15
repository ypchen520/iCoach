# import the timer I implemented here? maybe just the buttons
# a pomodoro design??
# I like a circular stopwatch

import streamlit as st
import time
from datetime import datetime
import pandas as pd
from utils import utils, auth

auth.authenticate()

def init_session_state():
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'break_counter' not in st.session_state:
        st.session_state.break_counter = 0
    if 'is_running' not in st.session_state:
        st.session_state.is_running = True
    if 'total_seconds' not in st.session_state:
        st.session_state.total_seconds = 0
    if 'sessions_history' not in st.session_state:
        st.session_state.sessions_history = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    remaining_seconds = seconds % 60
    return f'<div style=" \
                text-align: center; \
                color: LightCyan; \
                font-size: 60px; \
                font-family: Lucida Console, Courier New, monospace; \
            ">{hours}:{minutes:02d}:{remaining_seconds:02d}<div>'

def format_text(t):
    return f'<div style=" \
                text-align: center; \
                color: LightCyan; \
                font-size: 60px; \
                font-family: Lucida Console, Courier New, monospace; \
            ">{t}<div>'

def request_break():
    if st.session_state.is_running:
        st.session_state.break_counter += 1
        if st.session_state.break_counter >= 3:
            st.session_state.is_running = False
            # Save session data
            session_duration = st.session_state.total_seconds
            st.session_state.sessions_history.append({
                'start_time': st.session_state.start_time,
                'duration': session_duration,
                'breaks_requested': st.session_state.break_counter
            })

def reset_session():
    st.session_state.start_time = time.time()
    st.session_state.break_counter = 0
    st.session_state.is_running = True
    st.session_state.total_seconds = 0
    st.session_state.last_update = time.time()
    st.session_state.click_count = 0

@st.fragment(run_every="0.5s")
def timer():
    st.write(" ")
    time_placeholder = st.empty()
    
    # Update timer
    if st.session_state.is_running:
        current_time = time.time()
        st.session_state.total_seconds = int(current_time - st.session_state.start_time)
        
        # Rerun the app every second to update the timer
        # if current_time - st.session_state.last_update >= 1:
        st.session_state.last_update = current_time
        # time.sleep(1)  # Small delay to prevent too frequent updates
        # st.rerun(scope="fragment")
        # st.rerun(scope="fragment")
        time_placeholder.markdown(format_time(st.session_state.total_seconds), unsafe_allow_html=True)

image_path = "assets/cockpit.jpeg" 
utils.set_bg(image_path)

# Initialize session state
init_session_state()

# Create two columns for layout
# col1, col2 = st.columns(2)

# clock_container = st.empty()

# while True:
#     now = pendulum.now()
#     current_time = now.to_time_string()
#     clock = f'<span style="color: Black; font-size: 100px;">{current_time}<span>'
#     # st.markdown(clock, unsafe_allow_html=True)
#     clock_container.write(clock, unsafe_allow_html=True)
#     time.sleep(1)

# with col1:
timer()
    
# with col2:
# @st.fragment(run_every="0.1s")
# def tracker():
#     icons = ["⓵", "⭕", "❌", "✅"]  # Change icons as needed

#     if st.button(format_text(icons[st.session_state.click_count]), type="tertiary"):
#         if st.session_state.click_count < 3:
#             st.session_state.click_count += 1

# tracker()
custom_button_style = """
    <style>
        .stButton {
            display: flex;
            text-align: center;
        }
    </style>
    """

st.markdown(
    """
    <style>
        .element-container:has(style){
            display: none;
        }
        #button-after {
            display: none;
        }
        .element-container:has(#button-after) {
            display: none;
        }
        .element-container:has(#button-after) + div button {
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True)


@st.fragment(run_every="0.5s")
def tracker():

    # st.markdown(custom_button_style, unsafe_allow_html=True)
    
    # button_placeholder = st.empty()
    # button_placeholder.markdown(custom_button_style, unsafe_allow_html=True)

    icons = ["🎧", "🎲", "⭐️", "✅"]

    # [TODO]: implement a start and reset mechanism
    # after the dice icon, a random choice of icons

    # st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
    if st.button(icons[st.session_state.click_count], type="tertiary", use_container_width=True):
        if st.session_state.click_count == 0:
            reset_session()
        if st.session_state.click_count <= 3:
            st.session_state.click_count += 1
        if st.session_state.click_count == 4:
            reset_session()

    
    # if st.button(icons[st.session_state.click_count], type="tertiary"):
    #     if st.session_state.click_count < 3:
    #         st.session_state.click_count += 1
    

    # # JavaScript to update session state when clicking the button
    # js_code = f"""
    #     <script>
    #     function updateState() {{
    #         fetch('/_stcore/sse?click_count=' + {st.session_state.click_count + 1}, {{method: 'POST'}})
    #         .then(() => location.reload());
    #     }}
    #     </script>
    # """

    # # Display button as HTML with JavaScript click event
    # st.markdown(
    #     f"""
    #     {js_code}
    #     <div style="text-align: center">
    #     <button onclick="updateState()" style="background: none; border: none; font-size: 40px;">
    #         {icons[st.session_state.click_count]}
    #     </button>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

tracker()

# if st.session_state.is_running:
#     # Create a button that changes appearance based on break counter
#     button_label = f"Need a break? ({3 - st.session_state.break_counter} more clicks needed)"
#     if st.button(button_label, key='break_button', 
#                 help="Click when you're having trouble focusing"):
#         request_break()
        
#     # Show encouraging messages based on break counter
#     if st.session_state.break_counter > 0:
#         messages = [
#             "Keep going! You're doing great!",
#             "Almost there! Stay focused!",
#             "One last push! You can do it!"
#         ]
#         st.info(messages[st.session_state.break_counter - 1])
# else:
#     st.success("Time for a break! Well done! 🎉")
#     if st.button("Start New Session"):
#         reset_session()

# # Show session history
# if st.session_state.sessions_history:
#     st.markdown("---")
#     st.markdown("### 📊 Session History")
#     history_df = pd.DataFrame(st.session_state.sessions_history)
#     history_df['start_time'] = pd.to_datetime(history_df['start_time'])
#     history_df['duration_minutes'] = history_df['duration'] / 60
    
#     # Format the dataframe for display
#     display_df = history_df.copy()
#     display_df['start_time'] = display_df['start_time'].dt.strftime('%Y-%m-%d %H:%M')
#     display_df['duration'] = display_df['duration_minutes'].round(1).astype(str) + ' minutes'
#     display_df = display_df.drop('duration_minutes', axis=1)
    
#     st.dataframe(display_df)
