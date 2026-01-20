#Write multiple strings into a file
file = open("data.txt", "w")
file.writelines(["Hello\n", "Welcome to Rajkot\n", "What is your name?"])
file.close()
