import streamlit as st

st.set_page_config(page_title="Tracker", page_icon=":paw_prints:", layout="wide")

st.sidebar.header(":mag: View")

# Create a multiselect widget for the user to choose options
selected_options = st.sidebar.multiselect(
    'Select options:',
    ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Add New Option']
)

# Check if "Add New Option" is selected
if 'Add New Option' in selected_options:
    # Allow the user to input a new option
    new_option = st.text_input('Enter new option:')
    
    # Display the new option
    st.write('New Option:', new_option)

    # Add the new option to the list of selected options
    if new_option not in selected_options:
        selected_options.append(new_option)

# Display the selected options
st.write('You selected:', selected_options)

# Allow the user to input data based on the selected options
for option in selected_options:
    if option != 'Add New Option':
        user_input = st.text_input(f'Enter data for {option}:')

        # Do something with the user input (you can customize this based on your requirements)
        st.write(f'Input for {option}: {user_input}')
