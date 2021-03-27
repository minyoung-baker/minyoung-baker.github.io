import json

# Read old JSON.
with open("website_items.json", "r") as inj:
    j = json.load(inj)

with open("website_items.json", "w") as outj:
    json.dump(j, outj, indent=4)

