import requests
import streamlit as st


@st.cache
def get_db(filename):
    url = 'https://media.githubusercontent.com/media/asbabiy/hsescraper/main/app/posts.db'
    r = requests.get(url)

    with open(f'app/{filename}.db', 'wb') as db:
        db.write(r.content)

    return len(r.content)
