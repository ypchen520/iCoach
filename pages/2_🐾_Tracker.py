import streamlit as st
import pandas as pd
import numpy as np
from data_sources import firebase
from data_sources import models
from utils import utils
import logging
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from datetime import datetime
import pytz

# """
# Page config
# """

st.set_page_config(page_title="Tracker", page_icon=":paw_prints:", layout="wide")


# """
# Get db
# """
db = firebase.get_firestore_client()
user_id = "eagle"
user_doc_ref = db.collection("User").document(user_id)


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

def get_date(dt: datetime) -> str:
    # dt = datetime.fromisoformat(datetime_str)

    # Define the target timezone (e.g., 'America/New_York')
    target_timezone = pytz.timezone('America/New_York')

    # Convert the datetime object to the target timezone
    dt_target_timezone = dt.astimezone(target_timezone)

    # Extract the year, month, and day
    year = dt_target_timezone.year
    month = dt_target_timezone.month
    day = dt_target_timezone.day

    # Combine into the desired format (YYYY-MM-DD)
    date_str = f"{year:04d}-{month:02d}-{day:02d}"

    print(date_str)  # Output will be the date in the target timezone

    return date_str

if st.button(":rocket: Upload", type="primary"):
    utils.upload_csv_to_db(db, "daily.csv")

# """
# Tabs
# """

# st.write(datetime.now().time())
timezone = pytz.timezone("America/New_York")

datetime_obj = datetime(2025, 2, 24, 8, 0, 0)
st.write(datetime_obj)

# Define mood options
moods = [
    ["Happy", "Excited", "Grateful"],
    ["Relaxed", "Content", "Tired"],
    ["Unsure", "Bored", "Anxious"],
    ["Angry", "Stressed", "Sad"]
]

mood_emojies = [
    ["😊", "🤩", "🙏"],
    ["😌", "🙂", "🥱"],
    ["🤔", "😐", "😬"],
    ["😤", "😣", "😢"]
]

if 'initial_mood' not in st.session_state:
    st.session_state.initial_mood = set()

if 'mood_buttons' not in st.session_state:
    st.session_state.mood_buttons = {mood: False for mood in [mood for row in moods for mood in row]}

if 'final_mood' not in st.session_state:
    st.session_state.final_mood = set()

if 'final_mood_buttons' not in st.session_state:
    st.session_state.final_mood_buttons = {mood: False for mood in [mood for row in moods for mood in row]}

health_tab, career_tab, fashion_tab = st.tabs([":broccoli: Health", ":rocket: Career", ":dark_sunglasses: Fashion"])

with health_tab:
    health_aspect_collection_ref = user_doc_ref.collection("health")

    health_category = None
    health_subcategory = None
    health_item = None

    # get options from fb
    # health_category_options = [doc.id.title() for doc in health_aspect_collection_ref.get()] + ["Add New"]
    health_category_options = [doc.id.title() for doc in health_aspect_collection_ref.get()]
    health_category = st.selectbox(":hatched_chick: **Category**", health_category_options, index=None, key="health_category_options") 
    result = None
    # if health_category == "Add New":
    #     result = utils.add_form("category", user_ref=user_doc_ref)
    if health_category:
        health_category_doc_ref = health_aspect_collection_ref.document(health_category.lower())
        # health_subcategory_options = [collection.id.title() for collection in health_category_doc_ref.collections()] + ["Add New"]
        health_subcategory_options = [collection.id.title() for collection in health_category_doc_ref.collections()]
        health_subcategory = st.selectbox(":hatching_chick: **Subcategory**", health_subcategory_options, index=None, key="health_subcategory_options")
        # if health_subcategory == "Add New":
        #     result = utils.add_form("subcategory", user_ref=user_doc_ref)
        if health_subcategory:
            subcategory_collection_ref = health_category_doc_ref.collection(health_subcategory.lower())
            health_date_options = set()
            for doc in subcategory_collection_ref.get():
                health_date_options.add(get_date(doc.to_dict()["date"]))
            # health_date_options = ["Add New"] + list(health_date_options)
            health_date_options = ["Add New"] + list(health_date_options)
            health_date = st.selectbox(":date: **Date**", health_date_options, index=None, key="health_date_options")
            if health_date == "Add New":
                date = st.date_input("Date", value="today")
                count = st.number_input("Count")
                st.markdown("<style>button {float: right}</style>", unsafe_allow_html=True)
                if date and count and st.button("Save", icon=":material/mood:"):
                    # datetime_obj = datetime.combine(date, datetime.time(8, 0, 0)).astimezone(timezone)
                    datetime_obj = datetime(date.year, date.month, date.day, 8, 0, 0).astimezone(timezone)
                    entry = models.ResistanceEntry(
                        date=datetime_obj,
                        count=count,
                    )

                    doc_id = entry.date.isoformat()
                    subcategory_collection_ref.document(doc_id).set(entry.__dict__)
                    st.success(f"{health_subcategory} entry saved!")
                # result = utils.add_form("resistance", user_ref=user_doc_ref)
            elif health_date:
                pass
                # filter fb with brand, list the items
                # queries = [FieldFilter("brand", "==", brand)]
                # item_options = [doc.to_dict()["name"] for doc in subcategory_collection_ref.where(filter=BaseCompositeFilter("AND", queries)).stream()] + ["Add New"]
                # item_name = st.selectbox("**Name**", item_options, index=None, key="item_options")
    #             if item_name == "Add New":
    #                 result = utils.add_form("item", user_ref=user_doc_ref) # , items={"brand": brand}
    #             elif item_name:
    #                 # for doc in subcategory_collection_ref.where("brand", "==", brand).where("name", "==", item_name).stream():
    #                 #     st.write(doc.to_dict())
    #                 queries.append(FieldFilter("name", "==", item_name))
    #                 docs = subcategory_collection_ref.where(filter=BaseCompositeFilter("AND", queries)).stream()
    #                 # docs = subcategory_collection_ref.where("brand", "==", brand).where("name", "==", item_name).stream()
    #                 existing_item = models.Clothes()
    #                 existing_item.read_from_db(next(docs))
    #                 result = utils.add_form("update", user_ref=user_doc_ref, items=existing_item.__dict__)
    #                 if result:
    #                     # TODO: probably should do some sort of async implementation
    #                     existing_item.write_to_db(collection_ref=subcategory_collection_ref, data=result, existing=True)

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
                    existing_item = models.Clothes()
                    existing_item.read_from_db(next(docs))
                    result = utils.add_form("update", user_ref=user_doc_ref, items=existing_item.__dict__)
                    if result:
                        # TODO: probably should do some sort of async implementation
                        existing_item.write_to_db(collection_ref=subcategory_collection_ref, data=result, existing=True)
