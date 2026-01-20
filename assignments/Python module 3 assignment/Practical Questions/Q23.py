# Practical Question 23: Search for a word in a string using re.search()
import re

text = "Learning Python is fun"
if re.search("Python", text):
    print("Word found")
