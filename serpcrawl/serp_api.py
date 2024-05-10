import streamlit as st
import serpapi
import pandas as pd
import re

st.set_page_config(layout="wide")

st.title('Google Maps Search Results')

# Input fields
api_key = 'e3940ba16652ef030fcb5fa1778728a1b5232cb82d07892b7b50a1a016b302d0'      
url = st.text_input('Enter url')
match = re.search(r'@(-?\d+\.\d+,-?\d+\.\d+)', url)
if match:
    lang_lat = match.group(1)
    print(f"Latitude and Longitude: {lang_lat}")  # Debug print
    pattern = r"/search/([^/]+)/"
    match = re.search(pattern, url)
    if match:
        search_keyword = match.group(1)
        type_search = search_keyword.replace('+', ' ')
        print(f"Search Keyword: {type_search}")  # Debug print
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
                    'll': lang_lat,  # Ensure that the ll parameter is correctly formatted
                    # 'start': page_number * 20
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
            columns_to_keep = ['position', 'title', 'rating', 'reviews', 'type', 'address', 'phone', 'website']
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
    else:
        print("Check your URL again.")
else:
    print("Latitude and longitude not found in URL.")
