import pandas as pd
from sqlalchemy import Table, select, and_
from sqlalchemy.orm import Session
from sqlalchemy_views import CreateView, DropView


def get_data(query, con):
    return pd.read_sql(query, con)


def filter_rows(data: Table, session: Session, attrs: dict, date_range: tuple):
    filters = [data.columns[k].in_(v) for k, v in attrs.items() if v]
    records = select([data]).where(and_(*filters)).where(data.columns['date'].between(*date_range))

    return records
