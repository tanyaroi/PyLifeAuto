# Write a function that: 
#   - Downloads sample json file to disk
#   - Reads json file
#   - Prints all json content to screen


import wget
import json

def json_print():
    URL = "https://raw.githubusercontent.com/LearnWebCode/json-example/master/animals-3.json"
    
    testfile = wget.download(URL, bar=None)

    with open(testfile) as f:
        json_dict = json.load(f)

    print()
    for entry in json_dict:
        for like in entry["foods"]['likes']:
            print(like)
        for like in entry["foods"]['dislikes']:
            print(like)
    print()

json_print()