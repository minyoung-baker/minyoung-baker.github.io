import re
import json
from bs4 import BeautifulSoup

# Read old JSON.
with open("website_items.json.bak", "r") as inj:
    injson = json.load(inj)


# Process old details.
f = open("index.html", "r")

soup = BeautifulSoup(f, "html.parser")

results = soup.find(id="cards")
menuitems = results.find_all("div", class_="card")

m = {}
for menuitem in menuitems:
    img = menuitem.find("img")
    title = menuitem.find("h2")
    price = menuitem.find("p", class_="price")
    ingredients = menuitem.find("p", class_="ingredients")

    if "(" in price.text:
        price_value = re.search(r"\$(\d+)", price.text).group(1)
        price_notes = re.search(r"\((.*)\)", price.text).group(1)
    else:
        price_value = price.text
        price_notes = ""

    m[title.text] = {
        "categories": injson[title.text]["categories"],
        "price": price_value,
        "notes": price_notes,
        "ingredients": [i.strip() for i in ingredients.text.split(".")][:-1],
        "figure": str(img),
    }


with open("website_items.json", "w") as outj:
    json.dump(m, outj, indent=4)
