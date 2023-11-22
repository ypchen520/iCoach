import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def get_firestore_client():
    # if not firebase_admin._apps:
    try:
        # cred = credentials.Certificate(firestore_keys)
        # firebase_admin.initialize_app(cred)
        firestore_keys = dict(st.secrets["firebase"]["adminsdk"])
        db = firestore.Client.from_service_account_info(firestore_keys)
        return db
    except Exception as e:
        st.error(f"Error initializing Firestore client: {e}")
        return None
    # return firestore.client()
