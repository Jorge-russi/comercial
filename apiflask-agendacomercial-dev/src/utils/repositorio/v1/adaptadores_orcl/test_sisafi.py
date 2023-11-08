from utils.config_source.dot_properties_adapter import dot_properties_adapter
from utils.repositorio.v1.repositorio_orcl import repositorio_orcl
class test_sisafi_adapter(repositorio_orcl):
    
    def __init__(self) -> None:
        cfg:dot_properties_adapter = dot_properties_adapter()
        user=cfg.get_property('datasource.diez.usr')
        password=cfg.get_property('datasource.diez.pwd')
        dns=cfg.get_property('datasource.diez.dns')
        super().__init__(dns, user, password)