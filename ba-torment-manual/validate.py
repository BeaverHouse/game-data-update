import json

with open("ba-torment-manual/output/S70-total.json", "r") as file:
    new_data = json.load(file)

with open("ba-torment-manual/old/S70.json", "r") as file:
    old_data = json.load(file)

for key in ["filters", "assist_filters", "min_partys", "max_partys"]:
    assert str(new_data[key]) == str(old_data[key]), f"{key} is not equal, {new_data[key]} != {old_data[key]}"
for key2 in range(len(new_data["parties"])):
    new = new_data["parties"][key2]
    old = old_data["parties"][key2]
    del new["USER_ID"]
    del old["USER_ID"]
    assert str(new["PARTY_DATA"]) == str(old["PARTY_DATA"]), "PARTY_DATA is not equal"

print("Validation passed")

