### This is the driver for the streamlit app.
### Once downloaded, Streamlit app can be initiated from local machine by running "streamlit run main.py" in Terminal

import pandas as pd
import streamlit as st
import json
from datetime import datetime

file_path = 'data.json'

with open(file_path, 'r') as json_file:
    data = json.load(json_file)

data_dict = dict(list(data.items()))
edition_list = [(date, edition_info["Edition Link"]) for date, edition_info in data_dict.items()]

# Set page configuration to wide layout
st.set_page_config(layout="wide")

#Sidebar
with st.sidebar:
    st.title("Search Below to Filter")
    # for date, link in edition_list:
    #     st.write(f'<a href="{link}">{date}</a>', unsafe_allow_html=True)
    
    # st.divider()

    # Create a search box
    search_headline_query = st.text_input("Search by Headline")
    search_desc_query = st.text_input("Search by Description")


# St App Body
st.header("Data Is Plural - Dataset Search")
col1, col2 = st.columns([1,2])


# Filter data based on the search query
all_data = []
filtered_data = []

for date, edition_data in data.items():
    for dataset_name, dataset_info in edition_data["Edition Datasets"].items():
        all_data.append((date, dataset_name, dataset_info))

for date, edition_data in data.items():
    for dataset_name, dataset_info in edition_data["Edition Datasets"].items():
        if search_headline_query.lower() in dataset_info["Headline"].lower() and search_desc_query.lower() in dataset_info["Description"].lower():
            filtered_data.append((date, dataset_name, dataset_info))


with col1:
    st.subheader('Available Datasets')
    if not search_headline_query and not search_desc_query:
        used_data = all_data
    elif search_headline_query or search_desc_query:
        used_data = filtered_data
    st.write(f"Found {len(used_data)} results:")
    selected_datasets = []
    for date, dataset_name, dataset_info in used_data:
        # Add a checkbox for each dataset
        checkbox_selected = st.checkbox(f"**{dataset_info['Headline']}**", key=dataset_info['Headline'])
        if checkbox_selected:
            selected_datasets.append((date, dataset_name, dataset_info))
        st.write(f"Edition: {date}")
        st.markdown(
                        f"""
                        <a href="{edition_data['Edition Link']}">
                            Link to Data is Plural Site
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
        st.write("---")

# Display selected dataset in col2
with col2:
    st.subheader('Selected Dataset')

    if selected_datasets:
        for date, dataset_name, dataset_info in selected_datasets:
            st.markdown(f"**{dataset_info['Headline']}**")
            st.write(f"Date: {date}")
            st.markdown(f"{dataset_info['Description']}", unsafe_allow_html=True)
            st.write(f"Edition Link: {edition_data['Edition Link']}")
            st.divider()
