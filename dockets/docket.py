import datetime

class Docket(object):

    def __init__(self, name = None, layout_number = None):
        self.date = datetime.date.today()
        self.name = name
        self.layout_number = layout_number


# Redseign the pdf form
# implement necasary fields
# fill the form
