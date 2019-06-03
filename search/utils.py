import json


def get_json_data(file_path):
    """
    Return json data from given path file.
    """

    try:
        with open(file_path) as f:
            data = json.load(f)
    except:
        return None

    return data