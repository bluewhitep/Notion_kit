from dataclasses import dataclass, field

from .base import *
from .property_item import (
    Option,
    Group,
)
from ..CONTENTS import (
    FORMAT_TYPES,
    ROLLUP_FUNCTION_LIST,
    ROLLUP_TYPE_LIST,
)

# FC: Number
@dataclass
class Number(BaseMethod): 
    format: str = 'number'
    
    def __post_init__(self) -> None:
        assert self.format in FORMAT_TYPES, f"Format {self.format} is not in {FORMAT_TYPES}"
        super().__post_init__()
        
    def set_format(self, format):
        if format in FORMAT_TYPES:
            self.format = format
        else:
            assert format in FORMAT_TYPES, f"Format {self.format} is not in {FORMAT_TYPES}"
        super().asdict()
        
# FC: Formula
@dataclass
class Formula(BaseMethod): 
    expression: str = field(default_factory=str)

#--------------------------[Select \ Multi-Select \ Status]---------------------#
# FC: options
@dataclass
class Options(BaseMethod): 
    options: list[Option] = field(default_factory=list)

    def __post_init__(self) -> None:
        new_options = []
        for _,option in enumerate(self.options):
            if type(option) == dict:
                new_options.append(Option(**option))
            else:
                new_options.append(option)
        self.options = new_options
        super().__post_init__()

    def get_options_list(self) -> list[dict]:
        return [_.Dict for _ in self.options]
    
    def empty_options(self) -> None:
        self.options = []
        super().asdict()
    
    def append_option(self, option: Option) -> None:
        self.options.append(option)
        super().asdict()
      
# FC: groups
@dataclass
class Groups(BaseMethod): 
    groups: list[Group] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        new_groups = []
        for _, group in enumerate(self.groups):
            if type(group) == dict:
                new_groups.append(Group(**group))
            else:
                new_groups.append(group)
        self.groups = new_groups
        super().__post_init__()
    
    def get_groups_list(self) -> list[dict]:
        return [_.Dict for _ in self.groups]
    
    def empty_groups(self) -> None:
        self.groups = []
        super().asdict()
        
    def append_group(self, group: Group) -> None:
        self.groups.append(group)
        super().asdict()

# FC: status
@dataclass
class Status(BaseMethod): 
    groups: Groups = field(default_factory=Groups)
    options: Options = field(default_factory=Options)
    
    def __post_init__(self) -> None:
        if type(self.groups[0]) == dict:
            self.groups = Groups(self.groups)
        if type(self.options[0]) == dict:
            self.options = Options(self.options)
        super().__post_init__()

#--------------------------[Relation]---------------------#
# FC: Relation synced
@dataclass
class RelationSynced(BaseMethod): 
    synced_property_id: str = field(default_factory=str)
    synced_property_name: str = field(default_factory=str)
    
    def set_property_id(self, id:str):
        self.synced_property_id = id
        super().asdict()
    
    def set_property_name(self, name:str):
        self.synced_property_name = name
        super().asdict()
        
# FC: relation single
@dataclass
class RelationSingle(BaseMethod): 
    database_id: str = field(default_factory=str)
    single_property: dict = field(default_factory=dict)
    type: str = 'single_property'

    def set_database_id(self, id:str):
        self.database_id = id
        super().asdict()
        
# FC: relation dual   
@dataclass
class RelationDual(BaseMethod): 
    type: str = 'dual_property'
    database_id: str = field(default_factory=str)
    dual_property: RelationSynced = field(default_factory=RelationSynced)

    def __post_init__(self) -> None:
        if type(self.dual_property) == dict:
            self.dual_property = RelationSynced(**self.dual_property)
        super().__post_init__()

    def set_database_id(self, id:str):
        self.database_id = id
        super().asdict()
        
    def set_property(self, property:RelationSynced):
        property_of_type = type(property)
        if property_of_type == RelationSynced:
            self.dual_property = property
        elif property_of_type == dict:
            self.dual_property = RelationSynced(**property)
        else:
            ValueError(f"Property of type {property_of_type} is not supported")   
        super().asdict()
#--------------------------[Rollup]---------------------#
# FC: Rollup
@dataclass
class Rollup(BaseMethod):
    function: str = "show_original"
    relation_property_name: str = field(default_factory=str)
    relation_property_id: str = field(default_factory=str)
    rollup_property_name: str = field(default_factory=str)
    rollup_property_id: str = field(default_factory=str)
    
    def set_function(self, function:str):
        if function in ROLLUP_FUNCTION_LIST:
            self.function = function
        else:
            assert function in ROLLUP_FUNCTION_LIST, f"Function {function} is not in {ROLLUP_FUNCTION_LIST}"
        super().asdict()
        
    