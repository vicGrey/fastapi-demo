import json
from jsonschema import validate

with open("schema.json") as f:
    schema = json.load(f)

with open("data.json") as f:
    data = json.load(f)

validate(instance=data, schema=schema)

print("Validation passed")