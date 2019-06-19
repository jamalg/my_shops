import json


def read_json(file_path):
    with open(file_path) as f:
        data = f.read()
    return json.loads(data)
