import streamlit as st
import logging
from utils import auth, utils



# st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
auth.authenticate()

# st.write(auth.get_user_info())
# st.write(auth.is_authenticated())

st.set_page_config(page_title="My Life", page_icon=":eagle:", layout="wide")

st.title(":eagle: My Life")

image_path = "assets/eagle.jpeg" 
utils.set_bg(image_path)

with st.sidebar:
    auth.log_out()
