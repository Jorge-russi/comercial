import os

from .ports import iconfig_source

class enviroment_variable_adapter(iconfig_source):
    def get_property(self, key:str) -> str:
        return os.environ[key]
    
    def set_property(self, key:str, value:str) -> None:
        os.environ[key] = value