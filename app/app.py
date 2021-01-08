# --------------------------------------------------- Import Section ---------------------------------------------------

import re
from datetime import date
import sqlite3
from itertools import chain

import streamlit as st
import pandas as pd

from view import create_view
from supplementary import filter_rows

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy_views import CreateView
import sqlparse

# ------------------------------------------ Database Connection Establishing ------------------------------------------

conn = sqlite3.connect('app/posts.db')
conn.create_function('REGEXP', 2, lambda x, y: 1 if re.search(x, y) else 0, deterministic=True)
c = conn.cursor()
create_view('app/posts.db', 'data')

engine = create_engine('sqlite:///app/posts.db')
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
data = Table("data", metadata, autoload=True)

# ---------------------------------------------------- TODO Section ----------------------------------------------------

# починить даты V
# починить фильтры V
# починить рубрики V
# Починить излишнее количество строк из-за джойнов V
# Починить чтение бд V

# ------------------------------------------------- Filtering Section --------------------------------------------------

options = {}
for attr in ['campus', 'section', 'tag', 'person', 'branch']:
    with engine.connect() as con:
        option = con.execute(f"SELECT DISTINCT {attr} FROM data;")
        options[attr] = tuple(chain.from_iterable(option))

campus = st.sidebar.multiselect("Выберите кампус:", options['campus'], default=['Москва'])
tag = st.sidebar.multiselect('Выберите теги:', options['tag'], default=[])
branch = st.sidebar.multiselect('Выберите подразделения:', options['branch'], default=[])
section = st.sidebar.multiselect('Выберите рубрики:', options['section'], default=[])
person = st.sidebar.multiselect('Выберите людей:', options['person'], default=[])

date_range = st.sidebar.slider('Укажите временной диапазон:',
                               value=(date(2002, 9, 1), date.today()),
                               format='D.M.Y')

filters = {
    'campus': campus,
    'tag': tag,
    'branch': branch,
    'section': section,
    'person': person
}

filtered_view = Table('filtered_view', metadata)
filter_data = filter_rows(data, session, filters, date_range)
filter_view_query = CreateView(filtered_view, filter_data, temp=True).compile()

c.execute(str(filter_view_query))
conn.commit()

# -------------------------------------------------- First Page Section ------------------------------------------------


st.title('Статистика по запросу')

avg_text_len = c.execute('SELECT avg(length(text)) FROM filtered_view;').fetchone()[0]
news_count = c.execute('SELECT count(DISTINCT link) FROM filtered_view;').fetchone()[0]
popular_tag = c.execute('SELECT tag FROM filtered_view GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()
popular_section = c.execute('SELECT section FROM filtered_view GROUP BY section ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()
popular_branch = c.execute('SELECT branch FROM filtered_view GROUP BY branch ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()

stats = {
    'Количество постов': news_count,
    'Средняя длина поста': avg_text_len,
    'Самый распространённый тег': popular_tag,
    'Самая популярная рубрика': popular_section,
    'Самое упоминаемое подразделение': popular_branch
}

stats_df = pd.DataFrame(stats, index=['Статистика']).T
st.write(stats_df)

if show_stats_query := st.checkbox('Показать запрос'):
    st.code(sqlparse.format(str(filter_view_query), reindent=True), language='sql')

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

# conn.close()
