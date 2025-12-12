
import pandas as pd
from sqlalchemy import create_engine, text


def get_db_connection():
    """Establish and return a database connection"""
    # Implementation for database connection
    return create_engine('postgresql+psycopg2://postgres:password@localhost:5432/dvdrental');


def execute_query(sql_query):
    return pd.read_sql(sql_query, get_db_connection())