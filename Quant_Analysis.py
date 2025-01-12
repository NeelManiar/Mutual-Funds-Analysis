import pandas as pd
import streamlit as st

st.title('Changes in Mutual Fund Portfolios')

# Display a sample image for input instructions
st.image('/Users/ADMIN/Desktop/Sample Screenshot.png', caption='Sample image of the required file input', width=500)

# File uploader to accept multiple files (CSV/Excel)
uploaded_files = st.file_uploader(
    "Choose CSV or Excel files to compare 'NAME_OF_THE_INSTRUMENT'", 
    accept_multiple_files=True, 
    type=['csv', 'xlsx']
)

# Check if files have been uploaded
if uploaded_files:
    instrument_data = {}

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name  # Get the file name
        file_extension = file_name.split('.')[-1].lower()
        
        # Load the file based on its extension
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format for {file_name}")
            continue
        
        # Check if 'NAME_OF_THE_INSTRUMENT' exists in the file
        if 'NAME_OF_THE_INSTRUMENT' in df.columns:
            instrument_data[file_name] = set(df['NAME_OF_THE_INSTRUMENT'].dropna().unique())
        else:
            st.warning(f"'NAME_OF_THE_INSTRUMENT' not found in {file_name}")

    # Ensure there are at least two files for comparison
    if len(instrument_data) == 2:
        # Get a list of file names
        file_names = list(instrument_data.keys())

        # Get the instruments from the first and last files for comparison
        first_file, last_file = file_names[0], file_names[-1]
        first_file_data = instrument_data[first_file]
        last_file_data = instrument_data[last_file]

        # Find added and removed records using set operations
        added_records = (last_file_data - first_file_data)
        removed_records = (first_file_data - last_file_data)

        # Display results
        st.write(f"### Comparison Between '{first_file}' and '{last_file}'")
        st.write("**Records Added:**")
        st.write(added_records)
        st.write("**Records Removed:**")
        st.write(removed_records)
    else:
        st.warning("Please upload two files for comparison.")
else:
    st.warning("No files uploaded yet.")
