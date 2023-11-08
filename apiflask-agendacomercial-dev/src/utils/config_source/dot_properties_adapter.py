import configparser
import os
from .env_var_adapter import enviroment_variable_adapter

from .ports import iconfig_source

class dot_properties_adapter(iconfig_source):
    
    def __init__(self, file_path:str = None) -> None:
        super().__init__()
        if file_path is None:
            self.file_path = enviroment_variable_adapter().get_property('PRJS_CONF_FILE')
        else:
            self.file_path = file_path
    
    def get_property(self, key:str, section:str = 'default') -> str:
        config = configparser.RawConfigParser()
        config.read(self.file_path)
        property:str = config.get(section, key)
        return property
    
    def set_property(self, key:str, value:str, section:str = 'default') -> None:
        config = configparser.ConfigParser()
        config.read(self.file_path)
        config.set(section=section, option=key, value=value)
        with open(self.file_path, 'w') as configfile:
            config.write(configfile)
