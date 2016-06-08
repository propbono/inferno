from __future__ import print_function

from report import Report

import gspread
from oauth2client.service_account import ServiceAccountCredentials



SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'App Engine default service account'

def __get_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE,SCOPE)
    return credentials

def __get_worksheet(credentials):
    gc = gspread.authorize(credentials)
    spreadsheet_id = "1j1vJuOy3cGW-bzyr7MDjpMcD_L1DjCJOTOAruRb7JJo"
    sheet = gc.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet("Sheet2")
    return worksheet

def __get_values_in_order(row):
    return [[row["Date"], row["Name"], row["Layout"], row["Stock"],
             row["Stock "
                 "Size"],
             row["Printing Method"], row["Quantity"], row["Status"],
             row["Clients"], row["Notes"]] for key in row][0]

def add_reports_to_google():
    credentials = __get_credentials()

    worksheet = __get_worksheet(credentials)

    rows_count = worksheet.row_count
    report = Report()
    dictionary = report.return_dictionary()

    end_of_file = rows_count + 1
    for key in dictionary:
        values = __get_values_in_order(key)
        worksheet.insert_row(values, end_of_file)
        end_of_file += 1


if __name__ == "__main__":
    add_reports_to_google()

