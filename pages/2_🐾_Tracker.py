import streamlit as st
import pandas as pd
import numpy as np
from data_sources import firebase
from data_sources import model
from utils import utils
import logging
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter

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

    aspect_collection_ref = user_doc_ref.collection("fashion")

    category = None
    subcategory = None
    item = None
    brand = None

    # get options from fb
    category_options = [doc.id.title() for doc in aspect_collection_ref.get()] + ["Add New"]
    category = st.selectbox(":hatched_chick: **Category**", category_options, index=None, key="category_options") 
    result = None
    if category == "Add New":
        result = utils.add_form("category", user_ref=user_doc_ref)
    elif category:
        category_doc_ref = aspect_collection_ref.document(category.lower())
        subcategory_options = [collection.id.title() for collection in category_doc_ref.collections()] + ["Add New"]
        subcategory = st.selectbox(":hatching_chick: **Subcategory**", subcategory_options, index=None, key="subcategory_options")
        if subcategory == "Add New":
            result = utils.add_form("subcategory", user_ref=user_doc_ref)
        elif subcategory:
            subcategory_collection_ref = category_doc_ref.collection(subcategory.lower())
            brand_options = set()
            for doc in subcategory_collection_ref.get():
                brand_options.add(doc.to_dict()["brand"])
            brand_options = list(brand_options) + ["Add New"]
            brand = st.selectbox(":shirt: **Brand**", brand_options, index=None, key="brand_options")
            if brand == "Add New":
                result = utils.add_form("brand", user_ref=user_doc_ref)
            elif brand:
                # filter fb with brand, list the items
                queries = [FieldFilter("brand", "==", brand)]
                item_options = [doc.to_dict()["name"] for doc in subcategory_collection_ref.where(filter=BaseCompositeFilter("AND", queries)).stream()] + ["Add New"]
                item_name = st.selectbox("**Name**", item_options, index=None, key="item_options")
                if item_name == "Add New":
                    result = utils.add_form("item", user_ref=user_doc_ref) # , items={"brand": brand}
                elif item_name:
                    # for doc in subcategory_collection_ref.where("brand", "==", brand).where("name", "==", item_name).stream():
                    #     st.write(doc.to_dict())
                    queries.append(FieldFilter("name", "==", item_name))
                    docs = subcategory_collection_ref.where(filter=BaseCompositeFilter("AND", queries)).stream()
                    # docs = subcategory_collection_ref.where("brand", "==", brand).where("name", "==", item_name).stream()
                    existing_item = model.Clothes()
                    existing_item.read_from_db(next(docs))
                    result = utils.add_form("update", user_ref=user_doc_ref, items=existing_item.__dict__)
                    if result:
                        # TODO: probably should do some sort of async implementation
                        existing_item.write_to_db(collection_ref=subcategory_collection_ref, data=result, existing=True)
