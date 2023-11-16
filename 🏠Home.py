import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
# import pyexcel_ods
warnings.filterwarnings("ignore")
import pendulum

from google.cloud import firestore
import json

import utils

st.set_page_config(page_title="My Life", page_icon=":eagle:", layout="wide")

st.title(" :eagle: My Life")

st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

