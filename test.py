import re

text = '8/25/36'
print (re.findall(r"\d{1,3}(?:\.\d+)?", text))
