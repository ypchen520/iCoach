import streamlit as st
import numpy as np
from utils import gen

# Simulated database values (replace with actual database values)
db_values = np.random.randint(0, 100, size=(9, 9))
db_names = np.array([[gen.generate_random_string(5) for _ in range(9)] for _ in range(9)])

# Create a 9x9 grid
for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        with cols[j]:
            # Display an icon (e.g., a star)
            st.write(":avocado:")
            
            # Number input with default value from database
            st.number_input(db_names[i, j], value=db_values[i, j], key=f"{i}_{j}")