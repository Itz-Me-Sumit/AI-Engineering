import json
from pathlib import Path

def read_text(file_path):
    return Path(file_path).read_text(encoding = "utf-8")
    
def write_text(file_path , content):
    return Path(file_path).write_text(content , encoding = "utf-8")

def read_json(file_path) -> dict:
    with open(file_path , "r" , encoding = "utf-8") as file:
        return json.load(file)

def write_json(file_path , data:dict):
    with open(file_path , "r" , encoding = "utf-8") as file:
        json.dump(data , file , indent = 4)