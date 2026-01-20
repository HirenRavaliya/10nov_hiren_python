#Read contents of a file and print on console
file = open("sample.txt", "r")
content = file.read()
print(content)
file.close()
