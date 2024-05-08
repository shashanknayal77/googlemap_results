import streamlit as st
import serpapi
import pandas as pd

st.set_page_config(layout="wide")
st.title('Google Maps Search Results')

# Input fields
api_key = 'e4c319a9ebe06f54d3e99b82ec7605428a0b713b5b63f1167b2a992c966269cc'
type_search = st.text_input('Enter the search query:')       
lang_lat = st.text_input('Enter the latitude and longitude (e.g., @29.1769258,79.4507368,13z):')

# Create SERP API client
client = serpapi.Client(api_key=api_key)

if st.button('Fetch Results'):
    data = []
    page_number = 0
    index = 1
    while True:
        results = client.search({
            'engine': 'google_maps',
            'type': 'search',
            'q': type_search,
            'll': lang_lat,
            'start': page_number * 20
        })
        local_results = results.get("local_results", [])
        if not local_results:
            break
        for result in local_results:
            result['position'] = index
            data.append(result)
            index += 1
        page_number += 1

    df = pd.DataFrame(data)
    columns_to_keep = ['title', 'rating', 'reviews', 'unclaimed_listing', 'type', 'address', 'phone', 'website']
    df = df[columns_to_keep]
    # Display the results
    st.write(df)

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{type_search}.csv",
        mime='text/csv'
    )
