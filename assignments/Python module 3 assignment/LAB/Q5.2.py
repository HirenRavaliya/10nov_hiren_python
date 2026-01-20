#Handle multiple exceptions
try:
    file = open("test.txt", "r")
    print(file.read())
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print("Error:", e)
