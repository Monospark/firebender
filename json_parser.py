import os
import json


def parse_file(json_file, default_content=None):
    if default_content is not None:
        if not os.path.exists(json_file):
            f = open(json_file, "w")
            json.dump(default_content, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()
    with open(json_file) as f:
        data = json.load(f, object_hook=__json_unicode_to_str)
        return data


def __json_unicode_to_str(obj):
    if isinstance(obj, unicode):
        return str(obj)
    if isinstance(obj, list):
        return [__json_unicode_to_str(x) for x in obj]
    if isinstance(obj, dict):
        new_dictionary = {}
        for key, value in obj.iteritems():
            new_key = __json_unicode_to_str(key)
            new_value = __json_unicode_to_str(value)
            new_dictionary[new_key] = new_value
        return new_dictionary
    return obj
