import csv
import datetime
import os
import sys
from parse.parse import Parse
from configuration.configuration import Configuration

class Report(object):

    def __init__(self):

        self.headers = ["plated_date", "project_name", "printing_press", "layout_name", "stock_name", "notes", "stock_size", "printing_method", "quantity","status", "number_of_clients"]
        self.config = Configuration()
        self.products = {}

    def __generate_report(self, files_to_process):
        report = {}
        for file in files_to_process:
            try:
                # print_info_about_layouts()
                location = os.path.join(self.config.INPUT_DIR, file)
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

                    product_count = [p.name.split("-")[2] for p in layout.products]
                    row["number_of_clients"] = len(set(product_count))
                    report.setdefault("1", []).append(row)



            except Exception as e:
                print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        return report

    def save_report_to_csv(self):
        csv_file_name = os.path.join(os.path.join(self.config.OUTPUT_DIR,"report.csv"))
        report = self.__generate_report(self.config.FILES_TO_PROCESS)

        for key in report.keys():
            with open(csv_file_name, 'a', newline ='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = self.headers)
                writer.writeheader()
                writer.writerows(report[key])
        self._delete_processed_files(self.config.FILES_TO_PROCESS)

    def __generate_product_list(self, files_to_process):
        products = {}
        for file in files_to_process:
            try:

                # print_info_about_layouts()
                location = os.path.join(self.config.INPUT_DIR, file)
                date = self.__modification_date(location)
                xml = Parse(location)
                name = xml.get_project_name_bs4()
                for product in xml.products:
                    row = {}
                    row["date"] = date
                    row["name"] = name
                    row["upload"] = product.upload_number
                    row["client"] = product.name.split("-")[2]
                    row["size"] = product.width+"x"+product.height
                    row["stock"] = xml.get_project_stocks_bs4()[0].name
                    row["quantity"] = product.quantity
                    row["status"] = ""

                    products.setdefault("1", []).append(row)

            except Exception as e:
                print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        return products

    def __modification_date(self, filename):
        t = os.path.getmtime(filename)
        date = datetime.datetime.fromtimestamp(t)
        return date.strftime("%Y-%m-%d")

    def _delete_processed_files(self, FILES_TO_PROCESS):
        for file in FILES_TO_PROCESS:
            location = os.path.join(self.config.INPUT_DIR, file)
            os.remove(location)



