import sqlite3
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session


# conn = sqlite3.connect('../posts.db')
#
# engine = create_engine('sqlite:///posts.db')
# meta = MetaData(bind=engine)
# Session = sessionmaker(bind=engine)


def get_data(query, con):
    return pd.read_sql(query, con)


def filter_rows(data: Table, session: Session, attrs: dict):
    filters = [data.columns[k].in_(v) for k, v in attrs.items() if v]
    records = session.query(data).filter(*filters).all()

    df = pd.DataFrame.from_dict(records)
    df.index = pd.to_datetime(df.date, unit='ms')
    # df = df.drop('date', axis=1)
    # df = df.loc[:, ['tag']]
    df = df[['campus', 'section', 'tag', 'person', 'branch']]
    # df = df[['campus', 'section']]

    # return df
    return df
    # return df.drop_duplicates()
