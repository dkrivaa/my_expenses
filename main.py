"""
This program checks the bills reported in Morning against the expected bills - Companies
and number of bills - for each reporting period.
pip install requests, python-dotenv, streamlit
"""


import streamlit as st

login = st.Page(
    page='views/login.py',
    title='Login',
    default=True
)

expenses = st.Page(
    page='views/expenses.py',
    title='Expenses'
)

pg = st.navigation(pages=[login, expenses], position='hidden')
pg.run()
