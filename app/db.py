import requests
import streamlit as st


@st.cache
def get_db(filename):
    url = 'https://media.githubusercontent.com/media/asbabiy/hsescraper/main/app/posts.db'

    if not os.path.isfile(f"{filename}.db"):
        with open(f'app/{filename}.db', 'wb') as db:
            r = requests.get(url)
            db.write(r.content)

    # return len(r.content)
