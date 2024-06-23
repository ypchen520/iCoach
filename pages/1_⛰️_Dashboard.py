import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import numpy as np
warnings.filterwarnings("ignore")
import pendulum

import json

import utils.utils as utils

# credentials_path = "./adminsdk.json"
# db = firestore.Client.from_service_account_json(credentials_path)

# utils.upload_csv_to_db(db, "./daily.csv")

# doc_ref = db.collection("User").document("eagle")
# print(doc_ref)

# doc_data = doc_ref.get().to_dict()
# print(doc_data)

# # doc_ref = db.collection("User").document("eagle").collection("health").document("mental")
# # doc_ref.set({})

# doc_ref = db.collection("User").document("eagle").collection("career").document("ai")
# doc_ref.set({})

# """
# Categories: Health, Career, Self-Growth
# Subcategories: Resistance Training, Cardio, Sport, Mental Health
# Subcategories: Programming Language/Framework, ML/AI, Research, Job, Software Engineering
# Subcategories: Reading, Writing, Podcasts
# Subcategories:
# """

# chatbot
# dashboard
# motivational msg
# Huberman: goal setting
# meme: graphs + msg
# training seq data (can turn them into figures)
# seaborn

# fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls", "ods"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     if filename.endswith(".ods"):
#         pyexcel_ods.save_data(filename, "output.csv")
#     df = pd.read_csv("output.csv", encoding="ISO-8859-1")
# else:
#     current_dir = os.getcwd()
#     os.chdir(current_dir)
#     # pyexcel_ods.save_data("data.ods", "output.csv")
#     df = pd.read_csv("daily.csv", encoding="ISO-8859-1")
#     # print(df.head())

st.set_page_config(page_title="Dashboard", page_icon=":mountain:", layout="wide")

current_dir = os.getcwd()
os.chdir(current_dir)
# pyexcel_ods.save_data("data.ods", "output.csv")
df = pd.read_csv("daily.csv", encoding="ISO-8859-1")
# print(df.head())

col1, col2 = st.columns((2))

# get basketball
# bb_df = df[df["Task"] == "Basketball"]
# print(bb_df)

# get the min and max date
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()
# print(startDate)
# print(type(startDate))
# print(endDate)

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df_time = df[(pd.to_datetime(df["Date"]) >= date1) & (pd.to_datetime(df["Date"]) <= date2)].copy()

st.sidebar.header(":mag: View")

# category = st.sidebar.multiselect(":seedling: Root", df_time["Category"].unique())
# if not category:
#     df2 = df_time.copy()
# else:
#     df2 = df_time[df_time["Category"].isin(category)] # multiselect: using isin instead of "=="
category = st.sidebar.selectbox(":seedling: Root", df_time["Category"].unique())
if not category:
    df_category = df_time.copy()
else:
    df_category = df_time[df_time["Category"] == category] # multiselect: using isin instead of "=="

# subcategory = st.sidebar.multiselect(":wood: Branch", df2["Subcategory"].unique())
# if not subcategory:
#     df3 = df2.copy()
# else:
#     df3 = df2[df2["Subcategory"].isin(subcategory)]
subcategory = st.sidebar.selectbox(":wood: Branch", df_category["Subcategory"].unique())
if not subcategory:
    df_subcategory = df_category.copy()
else:
    df_subcategory = df_category[df_category["Subcategory"] == subcategory]


# task = st.sidebar.multiselect(":four_leaf_clover: Leaf", df3["Task"].unique())
tasks = st.sidebar.multiselect(":four_leaf_clover: Leaf", df_subcategory["Task"].unique())

_NUM_GRAPH_COLS = 2

rows = [tasks[i:i+_NUM_GRAPH_COLS] for i in range(0, len(tasks), _NUM_GRAPH_COLS)]
# st.write(rows)
for row in rows:
    cols = st.columns(_NUM_GRAPH_COLS)
    for col, task in zip(cols, row):
        # chart_data = pd.DataFrame(
        #     np.random.randn(20,3),
        #     columns=["a", "b", "c"]
        # )
        with col:
            st.write(task)
            df_task = df_subcategory[df_subcategory["Task"] == task]
            df_plot = df_task[["Date", "Count"]]

            # Ensure the Date column is of datetime type
            df_plot['Date'] = pd.to_datetime(df_plot['Date'])

            # Sort the DataFrame by Date
            df_plot.sort_values('Date', inplace=True)

            # Set the Date column as the index
            # df_plot.set_index('Date', inplace=True)

            # Convert string to int
            df_plot['Count'] = df_plot['Count'].astype(int)
            
            # st.line_chart(df_plot["Count"])

            st.line_chart(df_plot, x="Date", y="Count", use_container_width=True)

            # st.write(df_plot["Count"])
