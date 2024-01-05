import pandas as pd
import data_sources.model as model
import toml
import streamlit as st

# constants = toml.load("constants.toml")

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

def add_form(form_type="category", item=None):
    """
    Add a form for input based on the form type.
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
    for attr in model.Clothes.__dict__.keys():
        if not callable(getattr(model.Clothes, attr)) and not attr.startswith("_") and not attr.startswith("__") and attr != "id" and attr != "brand" and attr != "name":
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
        if not item:
            raise ValueError("An existing item should be provided for updating")
    
    with st.form("fashion_form"):
        st.markdown(custom_heading_style, unsafe_allow_html=True)
        st.subheader(":paw_prints: **Record**")
        # category = st.text_input("category", key="category")
        # item_name = st.text_input("name", key="item_name", placeholder="this is a placeholder", disabled=True)
        # brand = st.text_input("brand", key="brand")
        # 0:"category"
        # 1:"subcategory"
        # 2:"brand"
        # 3:"name"
        # 4:"date"
        # 5:"last_time"
        # 6:"color"
        # 7:"type"
        # 8:"frequency"
        # 9:"location"
        # 10:"madein"
        # 11:"count"
        # 12:"owned"
        # 13:"washed"
        result_dict = {}
        for entry in form_entries:
            if entry in {"date", "last_time"}:
                result_dict[entry] = st.date_input(entry)
            st.text_input(entry)
            
        
        submitted = st.form_submit_button("Submit") # TODO: customize the button
        if submitted:
            # user feedback
            item_name = "CLASS STR REPR"
            st.write(f"Tracked item: {item_name}")
            # res is a dict
            # TODO: use the form_entries as keys to create a dict
            # return res