import streamlit as st
import pandas as pd
import numpy as np
from data_sources import firebase
from data_sources import model
from utils import utils
import logging

st.set_page_config(page_title="Tracker", page_icon=":paw_prints:", layout="wide")

st.sidebar.header(":mag: View")

# firestore_keys = dict(st.secrets["firebase"]["adminsdk"])

# db = firestore.Client.from_service_account_info(firestore_keys)
# st.write(db)
db = firebase.get_firestore_client()
doc_ref = db.collection("User").document("eagle")
# st.write(doc_ref)
# st.write(doc_ref.get())
doc_data = doc_ref.get().to_dict()
st.write([attr for attr in model.Clothes.__dict__.keys() if not callable(getattr(model.Clothes, attr)) and not attr.startswith("__")])

# print(doc_data)

# db = firestore.Client.from_service_account_info(firestore_keys)
        
# # db = firebase.get_firestore_client()
# doc_ref = db.collection("User").document("eagle")

# doc_data = doc_ref.get().to_dict()
# st.write(doc_data)
# get options from fb

# add options to fb

# Create a multiselect widget for the user to choose options
selected_options = st.sidebar.multiselect(
    'Select options:',
    ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Add New Option']
)

# Check if "Add New Option" is selected
if 'Add New Option' in selected_options:
    # Allow the user to input a new option
    new_option = st.text_input('Enter new option:')
    
    # Display the new option
    st.write('New Option:', new_option)

    # Add the new option to the list of selected options
    if new_option not in selected_options:
        selected_options.append(new_option)

# Display the selected options
st.write('You selected:', selected_options)

# Allow the user to input data based on the selected options
for option in selected_options:
    if option != 'Add New Option':
        user_input = st.text_input(f'Enter data for {option}:')

        # Do something with the user input (you can customize this based on your requirements)
        st.write(f'Input for {option}: {user_input}')
