import json

def wrap_json_file(json_file):
    """Wraps the JSON file with '[', ']'

    Arguments:
        json_file {[type]} -- [description]
    """
    pass

with open("/home/derek/ray_results/SAC_2021-01-06_21-37-44/SAC_HalfCheetah-v3_5b337_00000_0_2021-01-06_21-37-44/result.json", "r") as f:
    results = json.load(f)
    print(type(results))
