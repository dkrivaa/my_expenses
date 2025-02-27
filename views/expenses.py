import streamlit as st
from datetime import datetime
import calendar

from expense_data import check_number_of_expenses, report_period


def dates():
    """ Getting relevant reporting period dates"""
    start_date, end_date = report_period()
    start = datetime.strptime(start_date, '%Y-%m-%d')
    start_name = start.strftime('%B')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    end_name = end.strftime('%B')
    year = datetime.strptime(end_date, '%Y-%m-%d').year

    return start_name, end_name, year


def year_options_list():
    current_year = datetime.now().year
    return list(range(current_year - 2, current_year + 5 + 1))


def make_new_report_date(year, months):
    options = ['Jan-Feb', 'Mar-Apr', 'May-June', 'July-Aug', 'Sep-Oct', 'Nov-Dec']
    last_month = options.index(months) * 2 + 2
    last_day = calendar.monthrange(year, last_month)[1]
    return f'{year}-{last_month}-{last_day}'


############# PAGE #############
def show_results(date=None):
    with st.container():
        st.subheader('Reporting Period:')
        start, end, year = dates()
        st.write(f'{start}-{end}, {year}')
        st.divider()

        lacking, shorts = check_number_of_expenses()
        st.subheader('Companies lacking bills altogether:')
        if len(lacking) > 0:
            for company in lacking:
                st.write(company)
        else:
            st.write('No Companies')
        st.subheader('Companies with less bills than expected:')
        if len(shorts) > 0:
            for company in shorts:
                st.write(company)
        else:
            st.write('No Companies')


show_results()
st.divider()

with st.form(key='change_report', clear_on_submit=True):
    st.subheader('Change Reporting Period:')
    year_options = year_options_list()
    new_year = st.selectbox('Choose Year', options=year_options)
    months = st.radio('Choose reporting months',
                      options=['Jan-Feb', 'Mar-Apr', 'May-June', 'July-Aug', 'Sep-Oct', 'Nov-Dec'],
                      index=None)

    if months is not None:
        submitted = st.form_submit_button('Submit')
        new_date = make_new_report_date(new_year, months)
        show_results(new_date)






