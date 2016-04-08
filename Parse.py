from xml.dom import minidom
import os
import pypdftk


from Layout import *
from bs4 import BeautifulSoup


from Stock import Stock
from ProductGroup import ProductGroup
from Product import Product


class Parse(object):
    def __init__(self, xml_location):
        self.stock_list = []
        self.product_groups = []
        self.products = []
        self.layouts = []
        self.project_name = ""

        try:
            self.xml = open(xml_location)
            self.soup = BeautifulSoup(self.xml.read())
        except IOError as e:
            self.xml = None
        else:
            self.printing_press = self.soup.find("press")["deviceid"]
            self.project_name = self.soup.project["projectid"]
            self.product_groups = self.get_product_groups_bs4()
            self.products = self.get_products_bs4()
            self.stock_list = self.get_project_stocks_bs4()


    def get_project_name_bs4(self):
        return self.project_name

    def get_project_stocks_bs4(self):
        stocks = self.soup.find_all("stocksheet")
        stock_name = self.soup.find("stock")['name']
        stock_list = []
        for s in stocks:
            stock = Stock()
            stock.width = s["width"]
            stock.height = s["height"]
            stock.ref_number = s["id"]
            stock.name = stock_name
            stock_list.append(stock)
        return stock_list

    def get_product_groups_bs4(self):
        groups = self.soup.find_all("productgroup")
        product_group_list = []
        for group in groups:
            ref_number = group["id"]
            name = group["name"]
            product_group_list.append(ProductGroup(ref_number,name))
        return product_group_list

    def get_printing_press_bs4(self):
        return self.printing_press

    def get_layouts_bs4(self):
        layouts = self.soup.find_all("layout")
        layout_list = []
        for layout_number, layout_soup in enumerate(layouts,1):
            layout = Layout()
            layout.name = "Layout-" + str(layout_number)
            layout.printing_method = layout_soup["printingmethod"]
            layout.quantity = layout_soup["sheetsrequired"]
            layout.press = self.printing_press
            layout.stock = self.__find_proper_stock(layout_soup)
            layout.percentage = layout_soup["percentagesheetuse"]
            layout.components = self.__find_products_for(layout_soup)
            layout.product_groups = self.__find_product_groups_for(layout.components)

            layout_list.append(layout)
        return layout_list

    def get_products_bs4(self):
        products = self.soup.find_all("product")
        product_list = []
        for product_soup in products:
            product = Product()
            product.name = product_soup["name"]
            product.width = product_soup["finishedtrimwidth"]
            product.height = product_soup["finishedtrimheight"]
            product.notes = product_soup["notes"]
            product.quantity = product_soup["requiredquantity"]
            product.upload_number = product_soup["description"]
            product.type = product_soup["type"]

            product.group = self.__find_product_group_for(product_soup)
            product.ref_number = product_soup.find("component")["id"]
            product.numberout = product_soup.find("component")[
                "requestednumberout"]

            product_list.append(product)
        return product_list

    def __find_proper_stock(self, layout):
        stock_ref = layout.find("stocksheetref")["rref"]
        for s in self.stock_list:
            if stock_ref == s.ref_number:
                return s

    def __find_products_for(self, layout):
        products_ref_list = layout.find_all("componentref")
        list_of_products = []
        for product_ref in products_ref_list:
            ref = product_ref["rref"]
            for product in self.products:
                if ref == product.ref_number:
                    list_of_products.append(product)
        return list_of_products

    def __find_product_groups_for(self, layout_components):
        # figure it out how to make set from list
        uniqe_product_group_list = {p.group for p in layout_components if
                                    p.group}
        return uniqe_product_group_list

    def __find_product_group_for(self, product_soup):
        product_group_ref = product_soup.find("productgroupref")

        if product_group_ref:
            ref_number = product_group_ref['rref']
            for product_group in self.product_groups:
                if ref_number == product_group.ref_number:
                    return product_group.name
        else:
            return None



files = [f for f in os.listdir() if f.endswith(".mxml")]

print("XML: BeautifulSoup")
for file in files:
    xml = Parse(file)
    print()
    print("Project Name: ", xml.get_project_name_bs4())
    print("Printing press: ", xml.get_printing_press_bs4())
    print("Project stocks: ")
    for stock in xml.get_project_stocks_bs4():
        print(" ",str(stock))

    print("Projects product groups: ")
    for group in xml.get_product_groups_bs4():
        print(" ",str(group))

    print("Project Layouts")
    for layout in xml.get_layouts_bs4():
        print(" Name: ", layout.name)
        print(" Quantity: ", layout.quantity)
        print(" Printing Method: ", layout.printing_method)
        print(" Press: ", layout.press)
        print(" Usage: ", layout.percentage)
        print(" Stock: ", layout.stock)
        print(" Layout groups: ")
        for group in layout.product_groups:
            print("     ", group)
        print(" Layout products: ")
        for product in layout.components:
            print("     ", product.name)



#xml.beauty()