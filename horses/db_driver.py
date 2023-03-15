import json

def write(x):
    with open("db.json", "w") as outfile:
        json.dump(x, outfile)

def read(x):
    with open("db.json", "r") as read_file:
        data = json.load(read_file)