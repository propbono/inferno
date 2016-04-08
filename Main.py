import os

from Parse import *

files = [f for f in os.listdir() if f.endswith(".mxml")]

xml = Parse(files[0])
xml.extract()

print(xml)