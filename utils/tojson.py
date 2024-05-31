import json
from codegen.classes import *

def toJson(node:Node) -> str:
    d = node.to_dict()
    json_str = json.dumps(d, indent=3)  # indent=4 for pretty printing
    print(json_str)
    with open("debug/json.txt", "w") as f:
            f.write(json_str)
    return json_str