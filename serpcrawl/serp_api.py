import streamlit as st
import serpapi
import pandas as pd
import re

# Set Streamlit page config
st.set_page_config(layout="wide")

# Streamlit app title
st.title('Google Maps Search Results')

# Input fields
api_key = 'e3940ba16652ef030fcb5fa1778728a1b5232cb82d07892b7b50a1a016b302d0'
url = st.text_input('Enter URL')
match = re.search(r'/search/([^/]+)/', url)
if match:
    search_keyword = match.group(1).replace('+', ' ')
    # st.write(f"Search Query: {search_keyword}")  # Display search query
    lang_lat_match = re.search(r'@(-?\d+\.\d+,-?\d+\.\d+,?\d*z)', url)
    if lang_lat_match:
        lang_lat = lang_lat_match.group()
        client = serpapi.Client(api_key=api_key)
        if st.button('Fetch Results'):
            try:
                data = []
                page_number = 0
                index = 1
                results = client.search({
                    'engine': 'google_maps',
                    'type': 'search',
                    'q': search_keyword,
                    'll': lang_lat,
                    # 'start': page_number * 20
                })
                local_results = results.get("local_results", [])
                for result in local_results:
                    result['position'] = index
                    data.append(result)
                    index += 1

                df = pd.DataFrame(data)
                required_columns = ['position', 'title', 'rating', 'reviews', 'type', 'address', 'phone', 'website']
                if all(col in df.columns for col in required_columns):
                    df = df[required_columns]

                # Display the results
                st.write(df)

                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv.encode(),
                    file_name=f"{search_keyword.replace(' ', '_')}_results.csv",
                    mime='text/csv'
                )
            except serpapi.SerpApiError as e:
                st.error(f"SerpApiError: {e}")
    else:
        st.warning("Latitude and longitude not found in URL.")
else:
    st.warning("")
