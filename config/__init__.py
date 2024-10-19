from json import load, dump
from os.path import exists

class Config:

    data : dict
    file : str

    def __init__(self, config_path:str) -> None:
        self.data = self.read_config(config_path)
        
    def read_config(self, config_path) -> dict:
        config : dict = {}
        self.file = config_path
        if exists(self.file):
            with open(self.file,'r') as file_io:
                config = load(file_io)
                file_io.close()
        return config

    def write_config(self, data):
        with open(self.file,'w') as file_io:
            dump(data, file_io, indent=4)
            file_io.close()
