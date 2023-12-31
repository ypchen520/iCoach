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

df = df[(pd.to_datetime(df["Date"]) >= date1) & (pd.to_datetime(df["Date"]) <= date2)].copy()

st.sidebar.header(":mag: View")

category = st.sidebar.multiselect(":seedling: Root", df["Category"].unique())
if not category:
    df2 = df.copy()
else:
    df2 = df[df["Category"].isin(category)] # multiselect: using isin instead of "=="

subcategory = st.sidebar.multiselect(":wood: Branch", df2["Subcategory"].unique())
if not subcategory:
    df3 = df2.copy()
else:
    df3 = df2[df2["Subcategory"].isin(subcategory)]


task = st.sidebar.multiselect(":four_leaf_clover: Leaf", df3["Task"].unique())
# print(type(task))

# Filter the data based on Category, Subcategory and Task

if not category and not subcategory and not task:
    filtered_df = df.copy()
elif not subcategory and not task:
    filtered_df = df2.copy()
elif not category and not task:
    filtered_df = df[df["Subcategory"].isin(subcategory)]
elif subcategory and task:
    filtered_df = df3[df["Subcategory"].isin(subcategory) & df["Task"].isin(task)]
elif category and task:
    filtered_df = df3[df["Category"].isin(category) & df3["Task"].isin(task)]
elif category and subcategory:
    filtered_df = df3[df["Category"].isin(category) & df3["Subcategory"].isin(subcategory)]
elif task:
    filtered_df = df3[df3["Task"].isin(task)]
else:
    filtered_df = df3[df3["Category"].isin(category) & df3["Subcategory"].isin(subcategory) & df3["Task"].isin(task)]


chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=["a", "b", "c"]
)

st.line_chart(chart_data)