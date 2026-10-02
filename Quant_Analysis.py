import pandas as pd
import streamlit as st

st.title('Changes in Mutual Fund Portfolios')

st.image('/Users/ADMIN/Desktop/Sample Screenshot.png', caption='Sample image of the required file input', width=500)

uploaded_files = st.file_uploader(
    "Choose CSV or Excel files to compare 'NAME_OF_THE_INSTRUMENT'", 
    accept_multiple_files=True, 
    type=['csv', 'xlsx']
)

if uploaded_files:
    instrument_data = {}

    
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
        
        # Checking if 'NAME_OF_THE_INSTRUMENT' is there or not
        if 'NAME_OF_THE_INSTRUMENT' in df.columns:
            instrument_data[file_name] = set(df['NAME_OF_THE_INSTRUMENT'].dropna().unique())
        else:
            st.warning(f"'NAME_OF_THE_INSTRUMENT' not found in {file_name}")

    
    if len(instrument_data) == 2:
        file_names = list(instrument_data.keys())

        first_file, last_file = file_names[0], file_names[-1]
        first_file_data = instrument_data[first_file]
        last_file_data = instrument_data[last_file]

        added_records = (last_file_data - first_file_data)
        removed_records = (first_file_data - last_file_data)

        st.write(f"### Comparison Between '{first_file}' and '{last_file}'")
        st.write("**Records Added:**")
        st.write(added_records)
        st.write("**Records Removed:**")
        st.write(removed_records)
    else:
        st.warning("Please upload two files for comparison.")
else:
    st.warning("No files uploaded yet.")
