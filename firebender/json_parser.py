import json
import os


def parse_json(json_file, default_content=None):
    if not os.path.exists(json_file):
        if default_content is not None:
            f = open(json_file, "w")
            json.dump(default_content, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()
        else:
            return None
    with open(json_file) as f:
        data = json.load(f)
        return data
