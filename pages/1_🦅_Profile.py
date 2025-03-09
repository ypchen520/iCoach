import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, firestore
from utils import sprite
from data_sources import firebase
import numpy as np
import pandas as pd
from PIL import Image
import base64
import time
import math

# Set page config
st.set_page_config(layout="wide") # page_title="Character Profile", 

# Custom CSS for styling with circular progress bars

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

# Path to your sprite sheet - replace with your actual path
sprite_sheet_path = "assets/Knights/Troops/Warrior/Purple/Warrior_Purple.png"
    
try:
    # Initialize Firebase
    db = firebase.get_firestore_client()
    
    # Placeholder user ID - in a real app, this would come from authentication
    user_id = "eagle"
    
    # Fetch todo data and calculate total experience
    # todo_data, total_exp = fetch_todo_data(db, user_id)
    todo_data = None
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
        level,
    )
    
    # Show total experience
    st.markdown(f"<h3 style='text-align:center;'>Total Experience: {total_exp} points</h3>", 
                unsafe_allow_html=True)
    
    # Display todos
    st.header("Todo Tasks")
    if todo_data:
        df = pd.DataFrame(todo_data)
        cols_to_display = ['title', 'description', 'exp', 'completed']
        cols_to_display = [col for col in cols_to_display if col in df.columns]
        
        st.dataframe(df[cols_to_display], use_container_width=True)
        
        # Display completed vs pending tasks
        completed_tasks = sum(1 for todo in todo_data if todo.get('completed', False))
        st.text(f"Completed Tasks: {completed_tasks}/{len(todo_data)}")
    else:
        st.info("No todo tasks found. Add some tasks to gain experience!")
    
    # Add floating character sprite (optional - uncomment to enable)
    # add_character_sprite(sprite_sheet_path, position='bottom-right', width=100)
        
except Exception as e:
    st.error(f"Error: {e}")
    st.info("If Firebase is not properly configured, please check your credentials and connection.")
        
except Exception as e:
    st.error(f"Error: {e}")
    st.info("If Firebase is not properly configured, please check your credentials and connection.")