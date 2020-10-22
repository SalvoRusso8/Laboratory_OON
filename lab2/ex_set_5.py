import pandas as pd
import json

print("ex. 1")
states = "./states.json"
with open(states, 'r') as read_file:
    python_dict = json.load(read_file)
    print(python_dict)

print("ex. 2")
python_object = {
    'name': 'David', 'class': 'I', 'age': '6'
}
with open("./obj_to_json.json","w") as write_file:
    json.dump(python_object, write_file)

print("ex. 3")
json_string = json.dumps(python_object)
print(json_string)

print("ex. 4")
with open("./obj_to_data_sorted.json", "w") as sorted_file:
    json.dump(python_dict, sorted_file, sort_keys=True, indent=4)
    print(json.dumps(python_dict, sort_keys=True, indent=4))

print("ex. 5")
for x in python_dict["states"]:
    del x["area_codes"]

with open("./states_clean.json", "w") as states_clean:
    json.dump(python_dict, states_clean, indent=4)


