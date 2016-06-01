from __future__ import print_function

import sys

from report import Report

import csv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials



SCOPE = 'https://www.googleapis.com/feeds'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE,SCOPE)
    return credentials

def get_report_sheet():
    credentials = get_credentials()
    gc = gspread.authorize(credentials)

    spreadsheet_id = "1j1vJuOy3cGW-bzyr7MDjpMcD_L1DjCJOTOAruRb7JJo"
    sheet = gc.open_by_key(spreadsheet_id).sheet1
    return sheet


def get_missing():
    path = os.path.join("N:\\" ,"OUT")
    full_path = os.path.join(path, "numbers_m.csv")
    # with open(full_path, 'rb') as csv_file:
    #     reader = csv.DictReader(csv_file, fieldnames="UploadNumber")
    #     # list = []
    #     # for i in reader:
    #     #     list.append(i)
    reader = csv.DictReader(open(full_path))
    return reader #list

def get_prepped():
    path = os.path.join("Q:\\")
    pdf_list = [p[:7] for p in sorted(os.listdir(path)) if
                    p.upper().startswith("U") and p.lower().endswith('.pdf')]

    return pdf_list


if __name__ == "__main__":
    report = Report()
    report.save_report_to_csv()

    #spreadsheet = get_report_sheet()


    # missing = get_missing()
    # products = get_prepped() #report.generate_product_list()
    # for miss in missing:
    #     if not miss["UploadNumber"] in products:
    #         print(miss["UploadNumber"])#missing.pop(miss)
    #         del missing[miss]



