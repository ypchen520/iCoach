import streamlit as st

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    st.header("A")
    st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")
    st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")
    st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")

with col2:
    st.header("B")
    st.image("https://eagles.org/wp-content/uploads/layerslider/HomepageSlider/Challenger-Gena-2-V2-copy-scaled.jpg")

with col3:
    st.header("C")
    st.image("https://eagles.org/wp-content/uploads/layerslider/HomepageSlider/Challenger-Gena-2-V2-copy-scaled.jpg")