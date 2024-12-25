import json

with open("./saves/item.rng","r") as f:
    itemData = json.load(f)
print(itemData)
input()