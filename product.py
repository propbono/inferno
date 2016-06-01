class Product(object):
    def __init__(self, name = None, ref_number = None, upload_number = None,
                 width = None, height = None, notes = None, typo = None,
                 quantity = None, group = None, numberout = None,
                 ):
        self.name = name
        self.ref_number = ref_number
        self.upload_number = upload_number
        self.width = width
        self.height = height
        self.notes = notes
        self.type = typo
        self.quantity = quantity
        self.group = group
        self.numberout = numberout