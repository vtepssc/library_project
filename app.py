import streamlit as st
import sqlite3
import pandas as pd

st.title("Library Dashboard")

conn = sqlite3.connect('library.db')
df = pd.read_sql_query("SELECT * FROM books", conn)
st.dataframe(df)
