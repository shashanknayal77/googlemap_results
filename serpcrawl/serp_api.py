import streamlit as st
import serpapi
import pandas as pd
import re

st.set_page_config(layout="wide")

st.title('Google Maps Search Results')

# Input fields
api_key = 'e3940ba16652ef030fcb5fa1778728a1b5232cb82d07892b7b50a1a016b302d0'      
url = st.text_input('Enter url')
match = re.search(r'@(-?\d+\.\d+,-?\d+\.\d+,?\d*z)', url)
lang_lat=""
type_search=""
if match:
    lang_lat = match.group()
else:
    print("Location part not found in URL.")

pattern = r"/search/([^/]+)/"
match = re.search(pattern, url)
if match:
    search_keyword = match.group(1)
    type_search=search_keyword.replace('+', ' ')
else:
    print("Check your URL again.")
# Create SERP API client
client = serpapi.Client(api_key=api_key)
data = []
page_number = 0
index = 1
results = client.search({
    'engine': 'google_maps',
    'type': 'search',
    'q': type_search,
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
st.write(df)

    # Download button
csv = df.to_csv(index=False)
st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{type_search}.csv",
        mime='text/csv'
    )
