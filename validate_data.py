import json

with open("schema.json") as f:
    schema = json.load(f)

with open("data.json") as f:
    data = json.load(f)

for field, expected_type in schema.items():

    if field not in data:
        raise ValueError(f"{field} is required")

    if expected_type == "string" and not isinstance(data[field], str):
        raise ValueError (f"{field} must be a string")

    if expected_type == "integer" and not isinstance(data[field], int):
        raise ValueError (f"[field] must be an integer")

for field in data:
    if field not in schema:
        raise ValueError(f"Unexpected field: {field}")

print ("Validation passed")