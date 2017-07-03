class Stock(object):
    def __init__(self, name = None, width = None, height = None, ref_number = None):
        self.name = name
        self.width = width
        self.height = height
        self.ref_number = ref_number

    def __str__(self):
        return self.name +", "+ self.height+"x"+ self.width