from dataclasses import dataclass, asdict, field

from ..CONTENTS import (
    TEXT_COLOR_LIST,
)
#--------------------------[Support function]---------------------#
def clear_empty_id(Dict:dict) ->None:
    if 'id' in Dict and Dict['id'] == '':
        Dict.pop('id')

def clear_empty_name(Dict:dict) ->None:
    if 'name' in Dict and Dict['name'] == '':
        Dict.pop('name')

def check_color(color):
    if color not in TEXT_COLOR_LIST:
        raise ValueError(f"Color {color} is not in {TEXT_COLOR_LIST}")

#--------------------------[Object]---------------------#
# FC: Object class generic method
@dataclass
class BaseMethod:
    def __post_init__(self) -> None:
        self.Dict = self.asdict()
                              
    def asdict(self) -> dict: 
        Dict = asdict(self) 
        clear_empty_id(Dict)
        clear_empty_name(Dict)
        return Dict

    def update(self):
        self.Dict = self.asdict()
       
# FC: Color
@dataclass
class Color(BaseMethod):
    color: str = 'default'
    
# FC: ID
@dataclass
class ID(BaseMethod):
    id: str = field(default_factory=str)