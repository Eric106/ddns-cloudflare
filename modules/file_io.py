from json import load, dump

def write(file_path:str ,text: str):
    with open(file_path, 'w') as file:
        file.write(text)
        file.close()

def read(file_path: str) -> str:
    content : str = ''
    with open(file_path, 'r') as file:
        content = file.read()
        file.close()
    return content

def dict2json(path_json: str , data:dict):
    with open(path_json,'w') as json_file:
        dump(data, json_file)
        json_file.close()

def json2dict(path_json: str):
    content = None
    with open(path_json,'r') as json_file:
        content = load(json_file)
        json_file.close()
    return content