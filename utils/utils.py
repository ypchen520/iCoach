import pandas as pd
from data_sources import model
import streamlit as st
from datetime import datetime, time
import pytz

timezone= pytz.timezone("America/New_York")

def upload_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    # print(df.head(5))
    for index, row in df.iterrows():
        date = pd.to_datetime(row["Date"])
        category = row["Category"]
        subcategory = row["Subcategory"]
        task = row["Task"]
        print(task)
        print(date)
        total = int(row["Total"]) if task != "Basketball" else row["Total"]
        model.Task(name=task, total=total, date=date)
        if index < 5:
            print(index)
            print(date)
            print(category)
            print(subcategory)
            print(task)
            print(total)
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
    for attr in model.Clothes.__dict__["__annotations__"].keys():
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
                if model.Clothes.__annotations__[entry] == str:
                    result_dict[entry] = st.text_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif model.Clothes.__annotations__[entry] == int:
                    result_dict[entry] = st.number_input(entry, value=items[entry], placeholder=items[entry]) if items and entry in items else st.text_input(entry)
                elif model.Clothes.__annotations__[entry] == datetime:
                    if not items:
                        result_dict[entry] = st.date_input(entry)
                    elif entry in items:
                        result_dict[entry] = st.date_input(entry, value=items[entry])
                        result_dict[entry] = datetime.combine(result_dict[entry], datetime.min.time()).astimezone(timezone)
                elif model.Clothes.__annotations__[entry] == dict:
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