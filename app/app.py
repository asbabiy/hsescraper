# ----------------------------------------------------Import Section----------------------------------------------------

import re
from datetime import date
import sqlite3
from itertools import chain

import streamlit as st
import pandas as pd
from view import create_view
from supplementary import get_data, filter_rows

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# -------------------------------------------Database Connection Establishing-------------------------------------------

conn = sqlite3.connect('app/posts.db')
conn.create_function('REGEXP', 2, lambda x, y: 1 if re.search(x, y) else 0)
c = conn.cursor()
create_view('app/posts.db', 'data')

engine = create_engine('sqlite:///app/posts.db')
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
data = Table("data", metadata, autoload=True)

# -----------------------------------------------------TODO Section-----------------------------------------------------

# починить даты TODO V
# починить фильтры TODO V
# починить рубрики TODO V
# Починить излишнее количество строк из-за джойнов TODO V
# Починить чтение бд

# --------------------------------------------------Filtering Section---------------------------------------------------

df = get_data("SELECT * FROM data;", conn)
df.index = pd.to_datetime(df.date)


options = {}
for attr in ['campus', 'section', 'tag', 'person', 'branch']:
    option = c.execute(f"SELECT DISTINCT {attr} FROM data;")
    options[attr] = tuple(chain.from_iterable(option))

campus = st.sidebar.multiselect("Выберите кампус:", options['campus'], default=['Москва'])
tag = st.sidebar.multiselect('Выберите теги:', options['tag'], default=[])
branch = st.sidebar.multiselect('Выберите подразделения:', options['branch'], default=[])
section = st.sidebar.multiselect('Выберите рубрики:', options['section'], default=[])
person = st.sidebar.multiselect('Выберите людей:', options['person'], default=[])

start_date, stop_date = st.sidebar.slider('Укажите временной диапазон:',
                                          value=(date(2002, 9, 1), date.today()),
                                          format='D.M.Y')

filters = {
    'campus': campus,
    'tag': tag,
    'branch': branch,
    'section': section,
    'person': person
}

# --------------------------------------------------First Page Section--------------------------------------------------

st.title('Статистика по запросу')
df = filter_rows(data, session, filters)

st.write('Кампус:', df[['campus']].max()[0])
st.write('Рубрика:', df[['section']].max()[0])
st.write('Тег:', df[['tag']].max()[0])
st.write('Человек:', df[['person']].max()[0])
st.write('Подразделение:', df[['branch']].max()[0])


st.title('Поиск фраз в новостях')
search_query = st.text_input('Введите искомое слово:')
use_regex = st.checkbox('Использовать регулярные выражения')
search_mode = {True: 'REGEXP', False: 'LIKE'}

search_result = c.execute('''
SELECT 
    title, campus, date, link
FROM post 
    LEFT JOIN meta AS m 
        ON post.id = m.id
WHERE text {} ?;
'''.format(search_mode[use_regex]), (search_query if use_regex else f"%{search_query}%",)).fetchall()

st.markdown(f'Записи, содержащие выражение `{search_query if search_query else "_"}`:')
news_df = pd.DataFrame(search_result, columns=['title', 'campus', 'date', 'link'])
st.dataframe(news_df.head())
st.write('Всего:', len(news_df), 'новостей')


conn.close()
