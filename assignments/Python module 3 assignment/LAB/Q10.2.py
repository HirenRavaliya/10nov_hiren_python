#Match a word using re.match()
import re

text = "Python programming"
result = re.match("Python", text)

if result:
    print("Match found")
