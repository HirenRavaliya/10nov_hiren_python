#Search a word using re.search()
import re

text = "Python is powerful"
result = re.search("Python", text)

if result:
    print("Word found")
