from parse import *
from report import Report
import csv

print("XML: BeautifulSoup")


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


    # missing = get_missing()
    # products = get_prepped() #report.generate_product_list()
    # for miss in missing:
    #     if not miss["UploadNumber"] in products:
    #         print(miss["UploadNumber"])#missing.pop(miss)
    #         del missing[miss]



