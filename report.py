import csv
import datetime
import os
import sys
from parse import Parse

class Report(object):

    def __init__(self, files_to_process = None):

        self.headers = ["Date", "Name", "Layout","Stock", "Stock Size",
                        "Printing Method", "Quantity","Status",
                        "Clients", "Notes"]

        self.program_dir = os.path.dirname(sys.argv[0])
        self.prepped_file = "N:\\"
        self.mxml_dir_out = os.path.join(self.prepped_file, "OUT")
        # self.mxml_dir_in = os.path.join(self.prepped_file, "IN")
        self.mxml_dir_in = os.path.join(self.program_dir, "mxml_source")
        self.files_to_process = files_to_process or self.__get_files_for_testing()
        self.products = []

    def __get_files_for_testing(self):
        return [f for f in os.listdir(
                self.mxml_dir_in) if f.endswith(".mxml")]

    def __generate_report(self, files_to_process):
        report = {}
        for file in files_to_process:
            try:
                location = os.path.join(self.mxml_dir_in, file)
                xml = Parse(location)
                project_name = xml.get_project_name_bs4()
                printing_press = xml.get_printing_press_bs4()
                date = self.__modification_date(location)

                for layout in xml.get_layouts_bs4():

                    row = {}
                    row["Date"] = date
                    row["Name"] = project_name
                    row["Layout"] = layout.name
                    row["Notes"] =""
                    for group in layout.product_groups:
                        row["Notes"] += " " + group
                    row["Stock"] = layout.stock.name
                    row["Stock Size"] = layout.stock.height + "x" + \
                                       layout.stock.width
                    row["Printing Method"] = layout.printing_method
                    row["Quantity"] = layout.quantity

                    product_count = [p.name.split("-")[2] for p in layout.products]
                    row["Clients"] = len(set(product_count))
                    row["Status"] = ""
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

    def return_dictionary(self):
        report = self.__generate_report(self.files_to_process)
        dictionary = [report[entry] for entry in report.keys()][0]
        return dictionary

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
        date = datetime.datetime.fromtimestamp(t)
        return date.strftime("%Y-%m-%d")



