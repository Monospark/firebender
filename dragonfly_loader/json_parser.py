import os
import json


def parse_json(json_file, default_content=None):
    if default_content is not None:
        if not os.path.exists(json_file):
            f = open(json_file, "w")
            json.dump(default_content, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()
    with open(json_file) as f:
        data = json.load(f)
        return data
