class ProductGroup(object):
    def __init__(self, ref_number, name):
        self.ref_number = ref_number
        self.name = name

    def __str__(self):
        return self.name