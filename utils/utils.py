import pandas as pd
from data_sources import models
import streamlit as st
from datetime import datetime, time
import pytz
import base64

timezone = pytz.timezone("America/New_York")

def rate_initial_mood(moods, mood_emojies, toggle_mood, session_state_mood_buttons, session_state_initial_moods):
    with st.container():
    # st.markdown(col_style, unsafe_allow_html=True)
        for i in range(len(moods)):
            row = moods[i]
            ncols = len(row)
            cols = st.columns(ncols, gap="small", vertical_alignment="center", border=True)
            for j in range(ncols):
                mood = moods[i][j]
                emoji = mood_emojies[i][j]
                if session_state_mood_buttons[mood]:
                    session_state_initial_moods.add(mood)
                    cols[j].button(mood, key=mood, icon=emoji, use_container_width=True, type="primary", on_click=toggle_mood, args=(mood, session_state_mood_buttons))
                else:
                    session_state_initial_moods.discard(mood)
                    cols[j].button(mood, key=mood, icon=emoji, use_container_width=True, type="tertiary", on_click=toggle_mood, args=(mood, session_state_mood_buttons))

def set_bg(main_bg):
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

def upload_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    # print(df.head(5))
    for index, row in df.iterrows():
        date = pd.to_datetime(row["Date"])
        category = row["Category"]
        subcategory = row["Subcategory"]
        task = row["Task"]
        count = int(row["Count"]) if task != "Basketball" else row["Count"]
        models.Resistance(date=date, count=count)
        if index < 90 and task == "Abs":
            st.write(index)
            st.write(date)
            st.write(category)
            st.write(subcategory)
            st.write(task)
            st.write(count)
        # print(type(row[["Date"]]))
        # print(row["Task"])

def add_form(form_type="category", user_ref=None, items=None):
    """
    Add a form for input based on the form type. Currently only supports the Fashion/Clothes category.
    Parameters:
    - form_type (str): category, subcategory, brand, item.
    - brand (str): brand name.
    - name (str): item name.

    Returns:
    dict: The form data

    Raise:
    - ValueError:
    """
    custom_heading_style = """
    <style>
        .stHeadingContainer {
            display: flex;
            text-align: center;
        }
        # }
    </style>
    """
    # Select entries based on the type of form specified
    form_entries = []
    ### model.Clothes.__annotations__
    # for attr in model.Clothes.__dict__.keys():
    #     if not callable(getattr(model.Clothes, attr)) and not attr.startswith("_") and not attr.startswith("__") and attr != "id" and attr != "brand" and attr != "name":
    #         form_entries.append(attr)
    for attr in models.Clothes.__dict__["__annotations__"].keys():
        if attr != "id" and attr != "brand" and attr != "name":
            form_entries.append(attr)

    if form_type == "category":
        form_entries = ["category", "subcategory", "brand", "name"] + form_entries
    elif form_type == "subcategory":
        form_entries = ["subcategory", "brand", "name"] + form_entries
    elif form_type == "brand":
        form_entries = ["brand", "name"] + form_entries
    elif form_type == "item":
        form_entries = ["name"] + form_entries
    elif form_type == "update":
        form_entries = ["name"] + form_entries
        if not items:
            raise ValueError("An existing item should be provided for updating")
    
    with st.form("fashion_form"):
        st.markdown(custom_heading_style, unsafe_allow_html=True)
        st.subheader(":paw_prints: **Record**")
        result_dict = {}
        for entry in form_entries:
            if entry in {"category", "subcategory", "brand"}:
                result_dict[entry] = st.text_input(entry)
            else:
                if models.Clothes.__annotations__[entry] == str:
                    result_dict[entry] = st.text_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif models.Clothes.__annotations__[entry] == int:
                    result_dict[entry] = st.number_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif models.Clothes.__annotations__[entry] == datetime:
                    if not items:
                        result_dict[entry] = st.date_input(entry)
                    elif entry in items:
                        result_dict[entry] = st.date_input(entry, value=items[entry])
                        result_dict[entry] = datetime.combine(result_dict[entry], datetime.min.time()).astimezone(timezone)
                elif models.Clothes.__annotations__[entry] == dict:
                    if items and entry in items:
                        result_dict[entry] = st.multiselect(entry, items[entry].keys())
                    elif user_ref:
                        result_dict[entry] = st.multiselect(entry, list(user_ref.get().to_dict()[entry]))
                    else:
                        result_dict[entry] = st.text_input(entry)
                        
        
        submitted = st.form_submit_button("Submit") # TODO: customize the button
        if submitted:
            return result_dict
            # user feedback
            # item_name = "CLASS STR REPR"
            # st.write(f"Tracked item: {item_name}")
            # res is a dict
            # TODO: use the form_entries as keys to create a dict
            # return res

def add_form(form_type="category", user_ref=None, items=None):
    """
    Add a form for input based on the form type. Currently only supports the Fashion/Clothes category.
    Parameters:
    - form_type (str): category, subcategory, brand, item.
    - brand (str): brand name.
    - name (str): item name.

    Returns:
    dict: The form data

    Raise:
    - ValueError:
    """
    custom_heading_style = """
    <style>
        .stHeadingContainer {
            display: flex;
            text-align: center;
        }
        # }
    </style>
    """
    # Select entries based on the type of form specified
    form_entries = []
    ### model.Clothes.__annotations__
    # for attr in model.Clothes.__dict__.keys():
    #     if not callable(getattr(model.Clothes, attr)) and not attr.startswith("_") and not attr.startswith("__") and attr != "id" and attr != "brand" and attr != "name":
    #         form_entries.append(attr)
    for attr in models.Clothes.__dict__["__annotations__"].keys():
        if attr != "id" and attr != "brand" and attr != "name":
            form_entries.append(attr)

    if form_type == "category":
        form_entries = ["category", "subcategory", "brand", "name"] + form_entries
    elif form_type == "subcategory":
        form_entries = ["subcategory", "brand", "name"] + form_entries
    elif form_type == "date":
        form_entries = ["date", "count"] + form_entries
    elif form_type == "item":
        form_entries = ["name"] + form_entries
    elif form_type == "update":
        form_entries = ["name"] + form_entries
        if not items:
            raise ValueError("An existing item should be provided for updating")
    
    with st.form("date_form"):
        st.markdown(custom_heading_style, unsafe_allow_html=True)
        st.subheader(":paw_prints: **Record**")
        result_dict = {}
        for entry in form_entries:
            if entry in {"category", "subcategory", "date"}:
                result_dict[entry] = st.text_input(entry)
            else:
                if models.Resistance.__annotations__[entry] == str:
                    result_dict[entry] = st.text_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif models.Resistance.__annotations__[entry] == int:
                    result_dict[entry] = st.number_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif models.Resistance.__annotations__[entry] == datetime:
                    if not items:
                        result_dict[entry] = st.date_input(entry)
                    elif entry in items:
                        result_dict[entry] = st.date_input(entry, value=items[entry])
                        result_dict[entry] = datetime.combine(result_dict[entry], datetime.min.time()).astimezone(timezone)
                elif models.Resistance.__annotations__[entry] == dict:
                    if items and entry in items:
                        result_dict[entry] = st.multiselect(entry, items[entry].keys())
                    elif user_ref:
                        result_dict[entry] = st.multiselect(entry, list(user_ref.get().to_dict()[entry]))
                    else:
                        result_dict[entry] = st.text_input(entry)
                        
        
        submitted = st.form_submit_button("Submit") # TODO: customize the button
        if submitted:
            return result_dict