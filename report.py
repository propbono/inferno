import csv
import datetime
import os
import sys
from parse import Parse

class Report(object):

    def __init__(self):

        self.headers = ["plated_date", "project_name", "printing_press", "layout_name", "stock_name", "notes", "stock_size", "printing_method", "quantity"]
        self.program_dir = os.path.dirname(sys.argv[0])
        self.prepped_file = "N:\\"
        self.mxml_dir_out = os.path.join(self.prepped_file, "OUT")
        self.mxml_dir_in = os.path.join(self.prepped_file, "IN")
        self.files_to_process = [f for f in os.listdir(self.mxml_dir_in) if f.endswith(".mxml")]
        self.products = []

    def __generate_report(self, files_to_process):
        report = {}
        for file in files_to_process:
            try:
                # print_info_about_layouts()
                location = os.path.join(self.mxml_dir_in, file)
                xml = Parse(location)
                project_name = xml.get_project_name_bs4()
                printing_press = xml.get_printing_press_bs4()
                date = self.__modification_date(location)

                for layout in xml.get_layouts_bs4():
                    row = {}
                    row["plated_date"] = date
                    row["project_name"] = project_name
                    row["printing_press"] = printing_press
                    row["layout_name"] = layout.name
                    row["stock_name"] = layout.stock.name
                    row["notes"] = [g + ", " for g in layout.product_groups]
                    row["stock_size"] = layout.stock.height + "x" + layout.stock.width
                    row["printing_method"] = layout.printing_method
                    row["quantity"] = layout.quantity
                    report.setdefault("1", []).append(row)

            except Exception as e:
                print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        return report

    def save_report_to_csv(self):
        csv_file_name = os.path.join(os.path.join(self.mxml_dir_out,"report.csv"))
        report = self.__generate_report(self.files_to_process)

        for key in report.keys():
            with open(csv_file_name, 'a', newline ='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = self.headers)
                writer.writeheader()
                writer.writerows(report[key])

    def generate_product_list(self):
        products = []
        for file in self.files_to_process:
            try:
                # print_info_about_layouts()
                location = os.path.join(self.mxml_dir_in, file)
                xml = Parse(location)
                for product in xml.products:
                     products.append(product.upload_number)

            except Exception as e:
                print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        return products

    def __modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)



