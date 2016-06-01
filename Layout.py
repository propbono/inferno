class Layout(object):
    def __init__(self, name = None, method = None, quantity = None,
                 list_of_products = None, press = None,
                 stock = None, percentage = None, product_groups = None):
        self.name = name
        self.printing_method = method
        self.quantity = quantity
        self.press = press
        self.stock = stock
        self.products = list_of_products
        self.percentage = percentage
        self.product_groups = product_groups
        
