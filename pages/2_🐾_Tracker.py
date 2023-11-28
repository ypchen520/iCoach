import streamlit as st
import pandas as pd
import numpy as np
from data_sources import firebase
from data_sources import model
from utils import utils
import logging

# """
# Page config
# """

st.set_page_config(page_title="Tracker", page_icon=":paw_prints:", layout="wide")


# """
# Get db
# """
db = firebase.get_firestore_client()
user_doc_ref = db.collection("User").document("eagle")


# """
# Sidebar
# """
# st.sidebar.header(":mag: View")

# # Create a multiselect widget for the user to choose options
# sidebar_selected_options = st.sidebar.multiselect(
#     'Select options:',
#     ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Add New Option']
# )

# # Check if "Add New Option" is selected
# if 'Add New Option' in sidebar_selected_options:
#     # Allow the user to input a new option
#     new_option = st.text_input('Enter new option:')
    
#     # Display the new option
#     st.write('New Option:', new_option)

#     # Add the new option to the list of selected options
#     if new_option not in sidebar_selected_options:
#         sidebar_selected_options.append(new_option)
    
#     # TODO: add options to fb

# Allow the user to input data based on the selected options
# for option in sidebar_selected_options:
#     if option != 'Add New Option':
#         user_input = st.text_input(f'Enter data for {option}:')

#         # Do something with the user input (you can customize this based on your requirements)
#         st.write(f'Input for {option}: {user_input}')

# """
# Tabs
# """

health_tab, career_tab, fashion_tab = st.tabs([":broccoli: Health", ":rocket: Career", ":dark_sunglasses: Fashion"])

with health_tab:
    # Display the selected options
    # st.write('You selected:', sidebar_selected_options)

    doc_data = user_doc_ref.get().to_dict()

    # get options from fb
    category_options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    subcategory_options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    item_options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    category = st.selectbox("Select options:", category_options, key=0)
    subcategory = st.selectbox("Select options:", subcategory_options, key=1)
    item = st.selectbox("Select options:", item_options + ["Add New"], key=2)
    if item == "Add New":
        item = st.text_input("Enter new item:", key=3)

    with st.form("my_form"):
        item_name = st.text_input("Enter new item:", key="name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            # user feedback
            st.write(f"Item name: {item_name}")
    
    # """
    # store to fb
    # """

with career_tab:
    pass

with fashion_tab:
    # st.write([attr for attr in model.Clothes.__dict__.keys() if not callable(getattr(model.Clothes, attr)) and not attr.startswith("__")])

    category_collection_ref = user_doc_ref.collection("fashion")
    # for doc in doc_data:
    #     st.write(doc.id)
    #     st.write(type(doc.id))
    # st.write(doc_data)

    # get options from fb
    # category_options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    subcategory_options = [doc.id.title() for doc in category_collection_ref.get()]
    subcategory = st.selectbox("Select options:", subcategory_options, key=7)

    item = None

    if subcategory:
        doc_id = subcategory.lower()
        # st.write(category_collection_ref.document(doc_id).collections())
        item_options = [collection.id.title() for collection in category_collection_ref.document(doc_id).collections()]
        item = st.selectbox("Select options:", item_options, key=8)
        # item = st.selectbox("Select options:", item_options + ["Add New"], key=8)
    # if item == "Add New":
    #     item = st.text_input("Enter new item:", key=9)

    with st.form("fashion_form"):
        item_name = st.text_input("Enter new item:", key="fashion_item_form")
        submitted = st.form_submit_button("Submit")
        if submitted:
            # user feedback
            st.write(f"Item name: {item_name}")
