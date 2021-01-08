import pandas as pd
from sqlalchemy import Table, select, and_
import streamlit as st


def get_data(query, con):
    return pd.read_sql(query, con)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def filter_rows(data: Table, attrs: dict, date_range: tuple):
    filters = [data.columns[k].in_(v) for k, v in attrs.items() if v]
    records = select([data]).where(and_(*filters)).where(data.columns['date'].between(*date_range))

    return records
