with open("error.txt", "r", encoding="utf-16le") as f:
    text = f.read()
print("... " + text[-1500:])
