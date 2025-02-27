import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import calendar


def get_token():
    """ Getting a JWT token"""
    load_dotenv()
    token_url = os.getenv('TOKEN_URL')
    morning_api_key = os.getenv('MORNING_API_KEY')
    morning_secret = os.getenv('MORNING_SECRET')

    data = {
        "id": morning_api_key,
        "secret": morning_secret
    }
    values = json.dumps(data, indent=4)  # Pretty-print JSON
    headers = {
          'Content-Type': 'application/json'
        }
    response = requests.post(url=token_url, data=values, headers=headers)

    return response.json()['token']


def report_period(date=None):
    """
    Determines the two-month reporting period for a given date.

    If the date is within the first 5 days of a reporting period,
    it returns the previous period.

    Args:
        date (datetime, optional): The date to check. Defaults to today's date.

    Returns:
        tuple: (start_date, end_date) of the reporting period.
    """
    if date is None:
        date = datetime.today()
    else:
        date = datetime.strptime(date, '%Y-%m-%d')

    year, month, day = date.year, date.month, date.day

    # Determine the normal reporting period
    start_month = ((month - 1) // 2) * 2 + 1  # 1, 3, 5, 7, 9, 11
    end_month = start_month + 1

    # Get last day of end_month
    last_day_of_end_month = calendar.monthrange(year, end_month)[1]

    # Define standard start and end dates
    start_date = datetime(year, start_month, 1)
    end_date = datetime(year, end_month, last_day_of_end_month)

    # Adjust for beginning of period (first 5 days → return previous period)
    if day <= 10:
        start_month -= 2
        end_month -= 2

    # Adjust for year change if shifting to previous period
    if start_month < 1:
        start_month += 12
        end_month += 12
        year -= 1

    # Get last day of adjusted end_month
    last_day_of_end_month = calendar.monthrange(year, end_month)[1]

    # Adjusted start and end dates
    start_date = datetime(year, start_month, 1)
    end_date = datetime(year, end_month, last_day_of_end_month)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def get_expenses(date=None):
    """ This function gets all the expenses for the upcoming / present reporting period """
    load_dotenv()
    expense_url = os.getenv('EXPENSE_URL')

    # Getting the JWT token
    token = get_token()

    # Getting upcoming / present reporting period
    fromDate, toDate = report_period(date)

    dates = {
        'fromDate': fromDate,
        'toDate': toDate,
    }
    # make json string
    values = json.dumps(dates)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url=expense_url, data=values, headers=headers)

    return response.json()


def expense_dict():
    """
    Function that returns a dict with companies and expected number of bills for each
    reporting period
    """
    return {
        'פלאפון תקשורת בע"מ': 2,
        'תאומי אורלי': 2,
        'פז חברת נפט בע"מ': 0,
        'אלקטרה פאוור סופרגז בע"מ': 1,
        'מי  מודיעין בע"מ': 1,
        'סלופארק טכנולוגיות': 2,
        'בזק החברה הישראלית לתקשורת בע"מ': 2,
        'דרך ארץ הייווייז (1997) בע"מ': 2,
        'חברת החשמל לישראל בעמ': 1,
        'ביטוח לאומי': 2,
        'רשות המיסים - מס הכנסה': 1,
        'רשות המיסים - מע"מ': 1,
    }


def check_number_of_expenses(date=None):
    """
    This function checks the number of bills for companies in expense_dict
    and if expected companies have bills
    """
    data = get_expenses(date)

    def count_func(company):
        return sum(1 for d in data['items'] if d.get("supplier", {}).get("name") == company)

    shorts = []
    lacking = []

    if data:
        # Checking if number of bills is as expected
        for exp in data['items']:
            company = exp['supplier']['name']
            count = count_func(company)
            expected = 0
            if company in list(expense_dict().keys()):
                expected = expense_dict()[company]

            if count < expected:
                shorts.append(f'{company}')

        # Checking if all expected companies have bills
        expected_companies = list(expense_dict().keys())
        actual_companies = list({d.get("supplier", {}).get("name") for d in data['items']
                                 if "supplier" in d})

        for company in expected_companies:
            if company not in actual_companies:
                lacking.append(f'{company}')

    return lacking, shorts





