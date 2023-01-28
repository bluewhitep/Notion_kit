####################################################################################
# MIT License
#
# Copyright (c) 2023 bluewhitep
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################
from dataclasses import dataclass, field, asdict

from .CONTENTS import (
    ALL_PROPERTIES_TYPES,
    ROLLUP_FUNCTION_LIST,
    ROLLUP_TYPE_LIST,
    TEXT_COLOR_LIST,
    FORMAT_TYPES,
    CODE_LANGUAGE_LIST,
    BLOCK_TYPE_LIST,
    BLOCK_CHILDREN_TYPES,
)

def clear_empty_id(Dict:dict) ->None:
    if 'id' in Dict and Dict['id'] == '':
        Dict.pop('id')

def clear_empty_name(Dict:dict) ->None:
    if 'name' in Dict and Dict['name'] == '':
        Dict.pop('name')

def check_color(color):
    if color not in TEXT_COLOR_LIST:
        raise ValueError(f"Color {color} is not in {TEXT_COLOR_LIST}")

# FC: [Base] object class generic method
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
        
# FC: [Base] color
@dataclass
class ColorMethod(BaseMethod):
    color: str = 'default'
    
#--------------------------[L1 Base: Database-property type ]---------------------#  
# FC: [L1 Base T] Number
@dataclass
class Number(BaseMethod): 
    format: str = 'number'
    
    def __post_init__(self) -> None:
        assert self.format in FORMAT_TYPES, f"Format {self.format} is not in {FORMAT_TYPES}"
        super().__post_init__()
        
# FC: [L1 Base T] formula
@dataclass
class Formula(BaseMethod): 
    expression: str = field(default_factory=str)

# FC: [L1 Base T/I] option base
@dataclass
class Option(BaseMethod): 
    id: str | None = field(default_factory=str)
    name: str = field(default_factory=str)
    color: str = field(default_factory=str)
    
# FC: [L1 Base T] group base
@dataclass
class Group(BaseMethod): 
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    color: str = field(default_factory=str)
    option_ids: list[str] = field(default_factory=list)
    
# FC: [L1 Base T] relation synced
@dataclass
class RelationSynced(BaseMethod): 
    synced_property_id: str = field(default_factory=str)
    synced_property_name: str = field(default_factory=str)

# FC: [L1 Base T] rollup
@dataclass
class Rollup(BaseMethod):
    function: str = "show_original"
    relation_property_name: str = field(default_factory=str)
    relation_property_id: str = field(default_factory=str)
    rollup_property_name: str = field(default_factory=str)
    rollup_property_id: str = field(default_factory=str)

#--------------------------[L1 Base: property item]---------------------#
# FC: [L1 Base I] Url
@dataclass
class Url(BaseMethod): 
    url: str = field(default_factory=str)
    
# FC: [L1 Base I] Icon
@dataclass
class Icon(BaseMethod): 
    type: str = 'emoji'
    emoji: str = field(default_factory=str)

# FC: [L1 Base I] parent
@dataclass
class Parent(BaseMethod): 
    type: str = field(default_factory=str)
    page_id: str = field(default_factory=str)
    database_id: str = field(default_factory=str)
    
    def asdict(self) -> dict:
        Dict = super().asdict()
        if Dict['type'] == 'page_id':
            Dict.pop('database_id')
        elif Dict['type'] == 'database_id':
            Dict.pop('page_id')
        return Dict
    
# FC: [L1 Base I] Email
@dataclass
class Email(BaseMethod): 
    email: str = field(default_factory=str) 
 
# FC: [L1 Base I] Date
@dataclass
class Date(BaseMethod): 
    start: str = field(default_factory=str)
    end: str | None = field(default_factory=str)
    time_zone: None = None
    
# FC: [L1 Base I] formula value
@dataclass
class FormulaValue(BaseMethod): 
    """
    FormulaValue
    
    Parameters:
        type        (str):      - The type of the formula result. [Default: "string"]
                                - Possible values are "string", "number", "boolean", and "date".
    """
    type: str = 'string'
    
    # formula result
    string: str | None = None
    number: float | None = None
    boolean: bool = False
    date: Date | None = None
    
    def __post_init__(self) -> None:
        if type(self.date) == dict:
            self.date = Date(**self.date) # type: ignore
        super().__post_init__()
    
    def __zip(self) -> dict:
        return dict(zip(["string", "number", "boolean", "date"],
                        [self.string, self.number, self.boolean, self.date]))
    
    def asdict(self) -> dict: 
        _zip_value = self.__zip()
        Dict = {'type': self.type,
                self.type: _zip_value[self.type].asdict() if type(_zip_value[self.type]) == Date else _zip_value[self.type] 
            }
        return Dict 

# FC: [L1 Base I] rollup item
@dataclass
class RollupItem(BaseMethod): 
    """
    RollupItem
    
    Parameters:
        type        (str):      - The type of the rollup result. [Default: "array"]
                                  Possible values are "number", "date", "array", "unsupported" and "incomplete"
        function    (str):      - The function used to calculate the rollup result. [Default: "show_original"]
                                  Possible values include: "count", "count_values", "empty", "not_empty", "unique", 
                                    "show_unique", "percent_empty", "percent_not_empty", "sum", "average", "median", 
                                    "min", "max", "range", "earliest_date", "latest_date", "date_range", "checked", 
                                    "unchecked", "percent_checked", "percent_unchecked", "count_per_group", "percent_per_group", 
                                    "show_original"
    
    Raise
        ValueError:   - If the "function" is not in the ROLLUP_FUNCTION_LIST
        ValueError:   - If the "type" is not in the ROLLUP_TYPE_LIST
    """
    function: str = "show_original"
        #count, count_values, empty, not_empty, unique, show_unique, percent_empty, percent_not_empty, sum, average, median, min, max, range, earliest_date, latest_date, date_range, checked, unchecked, percent_checked, percent_unchecked, count_per_group, percent_per_group, show_original
    type: str = "array"
        # "number", "date", "array", "unsupported" and "incomplete"
    
    number: int = 0
    date: Date | None = None
    array: list[dict] = field(default_factory=list) # [{type:value}]
    incomplete: dict = field(default_factory=dict)
      
    def __post_init__(self) -> None:
        if type(self.date) == dict:
            self.date = Date(**self.date) # type: ignore
        
        assert self.function in ROLLUP_FUNCTION_LIST, f"Function {self.function} is not in the {ROLLUP_FUNCTION_LIST}"
        assert self.type in ROLLUP_TYPE_LIST, f"Type {self.type} is not in the {ROLLUP_TYPE_LIST}"
        super().__post_init__()
    
    def __zip(self) -> dict:
        return dict(zip(["number", "date", "array", "incomplete"],
                        [self.number, self.date, self.array, self.incomplete])) 
        
    def asdict(self) -> dict: 
        _zip_value = self.__zip()
        Dict = {'type': self.type,
                'function': self.function,
                self.type: _zip_value[self.type].asdict() if type(_zip_value[self.type]) == Date else _zip_value[self.type]
            }
        return Dict

#--------------------------[User]---------------------#
# FC: [User] bot owner
@dataclass
class BotOwner(BaseMethod): 
    type: str = 'workspace'
    workspace: bool = True
    
# FC: [User] bot
@dataclass
class BotBase(BaseMethod): 
    owner: BotOwner = field(default_factory=BotOwner)
    workspace_name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.owner) == dict:
            self.owner = BotOwner(**self.owner) # type: ignore
        super().__post_init__()
       
# FC: [User] short object
@dataclass
class UserShort(BaseMethod): 
    id: str = field(default_factory=str)
    object: str = field(default_factory=str)

# FC: [User] user object 
@dataclass
class User(BaseMethod):
    avatar_url: str | None = field(default_factory=str)
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    object: str = 'user'
    person: Email = field(default_factory=Email)
    type: str = 'person'
    
    def __post_init__(self) -> None:
        if type(self.person) == dict:
            self.person = Email(**self.person) # type: ignore
        super().__post_init__()
        
# FC: [User] bot object
@dataclass
class Bot(BaseMethod):
    avatar_url: str | None = None
    bot: BotBase = field(default_factory=BotBase)
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    object: str = 'user'
    type: str = 'bot'
    
    def __post_init__(self) -> None:
        if type(self.bot) == dict:
            self.bot = BotBase(**self.bot) # type: ignore
        super().__post_init__()

#--------------------------[File]---------------------#
# FC: [file] upload
@dataclass
class Upload(BaseMethod): 
    url: str = field(default_factory=str)
    expiry_time: str = field(default_factory=str)
    
# FC: [file] object
@dataclass
class FileUpload(BaseMethod): 
    type: str = 'file'
    file: Upload = field(default_factory=Upload)
    name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.file) == dict:
            self.file = Upload(**self.file) # type: ignore
        super().__post_init__()

# FC: [file] object
@dataclass
class FileLink(BaseMethod): 
    type: str = 'external'
    external: Url = field(default_factory=Url)
    name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        self.external = Url(**self.external) if type(self.external) == dict else self.external # type: ignore
        super().__post_init__()

#--------------------------[Rich Text]---------------------#
# FC: [Text] content
@dataclass
class TextContent(BaseMethod): 
    content: str = field(default_factory=str)
    link: Url | None = None
    
    def __post_init__(self) -> None:
        if type(self.link) == dict:
            self.link = Url(**self.link) # type: ignore
        super().__post_init__()
    
    def text_dict(self, name:str="text"): 
        return {name: self.asdict()}
        
# FC: [Text] style
@dataclass
class TextStyle(BaseMethod):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str ="default"
    
    def __post_init__(self) -> None:
        check_color(self.color)
        super().__post_init__()
    
# FC: [Text] object
@dataclass
class RichText(BaseMethod): 
    type: str = "text"
    text: TextContent = field(default_factory=TextContent)
    annotations: TextStyle = field(default_factory=TextStyle)
    href: str | None = None
    plain_text: str | None = None
    
    def __post_init__(self) -> None:
        self.text = TextContent(**self.text) if type(self.text) == dict else self.text # type: ignore
        self.annotations = TextStyle(**self.annotations) if type(self.annotations) == dict else self.annotations # type: ignore
        self.href = self.text.link.url if self.text.link is not None else None
        self.plain_text = self.text.content
        super().__post_init__()

#--------------------------[L2 Base]---------------------#
# FC: [L2] title
@dataclass
class Title(BaseMethod): 
    title: list[RichText] = field(default_factory=list)

    def __post_init__(self) -> None:
        new_title = []
        for _,rich_text in enumerate(self.title):
            if type(rich_text) == dict:
                new_title.append(RichText(**rich_text)) # type: ignore
        self.title = new_title
        super().__post_init__()

# FC: [L2 Base] options
@dataclass
class Options(BaseMethod): 
    options: list[Option] = field(default_factory=list)

    def __post_init__(self) -> None:
        new_options = []
        for _,option in enumerate(self.options):
            if type(option) == dict:
                new_options.append(Option(**option)) # type: ignore
            else:
                new_options.append(option)
        self.options = new_options
        super().__post_init__()

    def get_options_list(self) -> list[dict]:
        return [_.Dict for _ in self.options]
    
# FC: [L2 Base] groups
@dataclass
class Groups(BaseMethod): 
    groups: list[Group] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        new_groups = []
        for _, group in enumerate(self.groups):
            if type(group) == dict:
                new_groups.append(Group(**group)) # type: ignore
            else:
                new_groups.append(group)
        self.groups = new_groups
        super().__post_init__()

# FC: [L2 Base] relation single
@dataclass
class RelationSingle(BaseMethod): 
    database_id: str = field(default_factory=str)
    single_property: dict = field(default_factory=dict)
    type: str = 'single_property'

# FC: [L2 Base] relation dual
@dataclass
class RelationDual(BaseMethod): 
    type: str = 'dual_property'
    database_id: str = field(default_factory=str)
    dual_property: RelationSynced = field(default_factory=RelationSynced)

    def __post_init__(self) -> None:
        if type(self.dual_property) == dict:
            self.dual_property = RelationSynced(**self.dual_property) # type: ignore
        super().__post_init__()

# FC: [L2 Base] status
@dataclass
class Status(BaseMethod): 
    groups: list[Group] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        new_groups = []
        for _, group in enumerate(self.groups):
            if type(group) == dict:
                new_groups.append(Group(**group)) # type: ignore
            else:
                new_groups.append(group)
        new_options = []
        for _,option in enumerate(self.options):
            if type(option) == dict:
                new_options.append(Option(**option)) # type: ignore
            else:
                new_options.append(option)
        self.options = new_options
        super().__post_init__()

#--------------------------[Request return]---------------------#
# FC: [Other] Request info
@dataclass
class RequestInfo(BaseMethod): 
    archived: bool = False
    cover: FileLink | None = None
    created_by: UserShort = field(default_factory=UserShort)
    created_time: str = field(default_factory=str)
    icon: Icon | None = None
    id: str = field(default_factory=str)
    last_edited_by: UserShort = field(default_factory=UserShort)
    last_edited_time: str = field(default_factory=str)
    parent: Parent = field(default_factory=Parent)
    url: Url = field(default_factory=Url)
    object: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.created_by) == dict:
            self.created_by = UserShort(**self.created_by) # type: ignore
        if type(self.last_edited_by) == dict:
            self.last_edited_by = UserShort(**self.last_edited_by) # type: ignore
        if type(self.parent) == dict:
            self.parent = Parent(**self.parent) # type: ignore
        if type(self.url) == dict:
            self.url = Url(**self.url) # type: ignore
        if type(self.icon) == dict:
            self.icon = Icon(**self.icon) # type: ignore
        if type(self.cover) == dict:
            self.cover = FileLink(**self.cover) # type: ignore
        super().__post_init__()

    def asdict(self) -> dict: 
        Dict = super().asdict()
        if Dict['cover'] is not None and Dict['cover']['name'] == '':
            Dict['cover'].pop('name')
            
        if Dict['parent']['type'] == 'database_id':
            Dict['parent'].pop('page_id')
        elif Dict['parent']['type'] == 'page_id':
            Dict['parent'].pop('database_id')
            
        return Dict

#--------------------------[Block Base]---------------------#

# FC: [Block Base] Retrieve request info base
@dataclass
class BlockBase(BaseMethod):
    archived: bool = False
    created_by: UserShort = field(default_factory=UserShort)
    created_time: str = field(default_factory=str)
    has_children: bool = False
    id: str = field(default_factory=str)
    last_edited_by: UserShort = field(default_factory=UserShort)
    last_edited_time: str = field(default_factory=str)
    object: str = 'block'
    parent: Parent = field(default_factory=Parent)
    
    def __post_init__(self) -> None:
        if type(self.parent) == dict:
            self.parent = Parent(**self.parent) # type: ignore
        if type(self.created_by) == dict:
            self.created_by = UserShort(**self.created_by) # type: ignore
        if type(self.last_edited_by) == dict:
            self.last_edited_by = UserShort(**self.last_edited_by) # type: ignore
        super().__post_init__()
        
    def asdict(self) -> dict:
        Dict = super().asdict()
        
        Dict['parent'] = self.parent if type(self.parent) == dict else self.parent.asdict()
        Dict['created_by'] = self.created_by if type(self.created_by) == dict else self.created_by.asdict()
        Dict['last_edited_by'] = self.last_edited_by if type(self.last_edited_by) == dict else self.last_edited_by.asdict()
            
        return Dict

# FC: [Block Base] Block ID
@dataclass
class BlockID(BaseMethod):
    block_id: str = field(default_factory=str)

# FC: [Blocl Base] paragraph base
@dataclass
class ParagraphBase(BaseMethod):
    """
    Raises:
        ValueError:  If the "color" is not in the TEXT_COLOR_LIST
    """
    rich_text: list[RichText] = field(default_factory=list)
    color: str = "default"
    
    def __post_init__(self) -> None:
        if self.color not in TEXT_COLOR_LIST:
            raise ValueError(f"Text color {self.color} is not in the TEXT_COLOR_LIST")
        self.rich_text = [RichText(**text) if type(text) == dict else text # type: ignore
                            for text in self.rich_text]
        super().__post_init__()

# FC: [Blocl Base] paragraph text base
@dataclass
class Paragraph(ParagraphBase):
    pass

# FC: [Block Base] heading_1
@dataclass
class Heading(ParagraphBase):
    is_toggleable: bool = False

# FC: [Block Base] callout
@dataclass
class Callout(ParagraphBase):
    icon: Icon = field(default_factory=Icon)
    
    def __post_init__(self) -> None: 
        self.icon = Icon(**self.icon) if type(self.icon) == dict else self.icon # type: ignore
        super().__post_init__()

# FC: [Block Base] quote
@dataclass
class Quote(ParagraphBase):
    pass

# FC: [Block Base] bulleted_list_item
@dataclass
class BulletedListItem(ParagraphBase):
    pass

# FC: [Block Base] number_list_item
@dataclass
class NumberedListItem(ParagraphBase):
    pass

# FC: [Block Base] to_do
@dataclass
class ToDo(ParagraphBase):
    checked: bool = False
    
# FC: [Block Base] toggle
@dataclass
class Toggle(ParagraphBase):
    pass
    
# FC: [Block Base] code
@dataclass
class Code(BaseMethod):
    """
    Raises:
        ValueError:  If the "color" is not in the TEXT_COLOR_LIST
    """
    rich_text: list[RichText] = field(default_factory=list)
    caption: list[RichText] = field(default_factory=list)
    language: str = "python"
    
    def __post_init__(self) -> None:
        if self.language not in CODE_LANGUAGE_LIST:
            raise ValueError(f"Text color {self.language} is not in the CODE_LANGUAGE_LIST")
        self.rich_text = [RichText(**text) if type(text) == dict else text # type: ignore
                            for text in self.rich_text]
        self.caption = [RichText(**text) if type(text) == dict else text # type: ignore
                            for text in self.caption]
        super().__post_init__()

# FC: [Block Base] child_page
@dataclass
class ChildPage(BaseMethod):
    title: str = field(default_factory=str)

# FC: [Block Base] child_database
@dataclass
class ChildDatabase(BaseMethod):
    title: str = field(default_factory=str)

# FC: [Block Base] expression
@dataclass
class Expression(BaseMethod):
    expression: str = field(default_factory=str)

# FC: [Block Base] template
@dataclass
class Template(BaseMethod):
    rich_text: list[RichText] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.rich_text = [RichText(**text) if type(text) == dict else text # type: ignore
                            for text in self.rich_text]
        super().__post_init__()

# FC: [Block Base] link_to
@dataclass
class LinkTo(Parent):
    pass

# FC: [Block Base] synced block
@dataclass
class SyncedBlock(BaseMethod):
    synced_from: BlockID | None = None

    def __post_init__(self) -> None:
        if self.synced_from is not None:
            self.synced_from = BlockID(**self.synced_from) if type(self.synced_from) == dict else self.synced_from # type: ignore
        super().__post_init__()
    
# FC: [Block Base] table
@dataclass
class Table(BaseMethod):
    table_width: int = field(default_factory=int)
    has_column_header: bool = False
    has_row_header: bool = False
    
# FC: [Block Base] table row
@dataclass
class TableRow(BaseMethod):
    cells: list[list[RichText]] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.cells = [[RichText(**text) if len(text) != 0 and type(text) == dict  else text # type: ignore
                       for text in cell] for cell in self.cells]

#--------------------------[Property]---------------------#
# FC: [L2 Base] property type
@dataclass
class PropertyType(BaseMethod): 
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    type: str = 'title'
    
    # NOTE: Property type value
    # Because the value of key is type
    checkbox: dict = field(default_factory=dict)
    created_by: dict = field(default_factory=dict)
    created_time: dict = field(default_factory=dict)
    date: dict = field(default_factory=dict)
    email: dict = field(default_factory=dict)
    files: dict = field(default_factory=dict)
    formula: Formula = field(default_factory=Formula)
    last_edited_by: dict = field(default_factory=dict)
    last_edited_time: dict = field(default_factory=dict)
    multi_select: Options = field(default_factory=Options)
    title: dict | list[RichText] = field(default_factory=dict)
    number: Number = field(default_factory=Number)
    people: dict = field(default_factory=dict)
    phone_number: dict = field(default_factory=dict)
    relation: RelationSingle | RelationDual = field(default_factory=RelationSingle)
    select: Options = field(default_factory=Options)
    status: Status | dict = field(default_factory=dict)
    rich_text: dict = field(default_factory=dict)
    url:dict = field(default_factory=dict)
    rollup: Rollup = field(default_factory=Rollup)
        
    def __post_init__(self) -> None:
        if type(self.formula) == dict:
            self.formula = Formula(**self.formula) # type: ignore
        if type(self.relation) == dict:
            self.relation = RelationDual(**self.relation) if self.relation['type'] == 'dual_property' else RelationSingle(**self.relation)  # type: ignore
        if type(self.select) == dict:
            self.select = Options(**self.select)  # type: ignore
        if type(self.multi_select) == dict:
            self.multi_select = Options(**self.multi_select)  # type: ignore
        if type(self.status) == dict and self.status != {}:
            self.status = Status(**self.status)  # type: ignore
        if type(self.number) == dict:
            self.number = Number(**self.number)  # type: ignore
        if type(self.rollup) == dict:
            self.rollup = Rollup(**self.rollup)  # type: ignore
        if type(self.title) == list:
            new_title = []
            for _,rich_text in enumerate(self.title):
                if type(rich_text) == dict:
                    new_title.append(RichText(**rich_text))  # type: ignore
            self.title = new_title
        super().__post_init__()
    
    def __zip(self) -> dict: 
        return dict(zip(ALL_PROPERTIES_TYPES,
                        [self.title, self.rich_text, self.number, self.select, 
                        self.multi_select, self.status, self.date, self.people, 
                        self.files, self.checkbox, self.url, self.email, 
                        self.phone_number, self.relation, self.formula, 
                        self.rollup, self.created_time, self.created_by, 
                        self.last_edited_time, self.last_edited_by,
                        ]))
    
    def asdict(self) -> dict: 
        _zip_value = self.__zip()
        if type(_zip_value[self.type]) == dict:
            value = _zip_value[self.type]
        elif type(_zip_value[self.type]) == list:
            value = [_.asdict() for _ in _zip_value[self.type]]
        else:
            value = _zip_value[self.type].asdict()
        
        if 'options' in value or 'groups' in value:
            for _, options in value.items():  # type: ignore
                for option in options:
                    clear_empty_id(option)

        Dict = {
                "id": self.id,
                "name": self.name,
                "type": self.type,
                self.type: value,
        }
        clear_empty_id(Dict)
        return Dict

    def full_dict(self) -> dict: 
        return {self.name: self.asdict()}

    def label_dict(self) -> dict:
        return {'name': self.name,
                'type': self.type,
                'id': self.id,
                }
    
    def rename(self, new_name: str) -> None:
        self.name = new_name
        
# FC: [L2 Base] property Item
@dataclass
class PropertyItem(BaseMethod): 
    has_more: bool = False # NOTE: This is onlt for relation
    id: str = field(default_factory=str)
    type: str = field(default_factory=str)
    
    # NOTE: Property value
    title: list[RichText] = field(default_factory=list)
    rich_text: list[RichText] = field(default_factory=list)
    number: int | float | None = None
    select: Option | None = None
    multi_select: list[Option] = field(default_factory=list) 
    status: Option | None = None
    date: Date | None = None
    people: list[User] = field(default_factory=list)
    files: list[FileLink | FileUpload ] = field(default_factory=list)
    checkbox: bool = False
    url: str | None = None
    email: str | None = None
    phone_number: str | None = None
    relation: list[dict] = field(default_factory=list) # Example: [{'id': str}, ...]
    formula: FormulaValue = field(default_factory=FormulaValue)
    rollup: RollupItem = field(default_factory=RollupItem)
    created_by: User | Bot = field(default_factory=User)
    created_time: str = field(default_factory=str)
    last_edited_by: User | Bot = field(default_factory=User)
    last_edited_time: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.created_by) == dict:
            self.created_by = Bot(**self.created_by) if self.created_by['type'] == 'bot' else User(**self.created_by) # type: ignore
        if type(self.date) == dict:
            self.date = Date(**self.date) # type: ignore
        if type(self.files) == list:
            new_files = []
            for file in self.files:
                if type(file) == dict and file['type'] == 'file': # type: ignore
                    new_files.append(FileUpload(**file)) # type: ignore
                elif type(file) == dict and file['type'] == 'external': # type: ignore
                    new_files.append(FileLink(**file)) # type: ignore
                else:
                    new_files.append(file)
            self.files = new_files
        if type(self.last_edited_by) == dict:
            self.last_edited_by = Bot(**self.last_edited_by) if self.last_edited_by['type'] == 'bot' else User(**self.last_edited_by) # type: ignore
        if type(self.formula) == dict:
            self.formula = FormulaValue(**self.formula) # type: ignore
        if type(self.multi_select) == list:
            new_multi_select = []
            for option in self.multi_select:
                if type(option) == dict:
                    new_multi_select.append(Option(**option)) # type: ignore
                else:
                    new_multi_select.append(option)
            self.multi_select = new_multi_select
        if type(self.title) == list:
            new_title = []
            for _,rich_text in enumerate(self.title):
                if type(rich_text) == dict:
                    new_title.append(RichText(**rich_text)) # type: ignore
                else:
                    new_title.append(rich_text)
            self.title = new_title
        if type(self.people) == list:
            new_people = []
            for user in self.people:
                if type(user) == dict:
                    new_people.append(User(**user)) # type: ignore
                else:
                    new_people.append(user)
            self.people = new_people
        if type(self.rollup) == dict:
            self.rollup = RollupItem(**self.rollup) # type: ignore
        if type(self.select) == dict:
            self.select = Option(**self.select) # type: ignore
        if type(self.status) == dict:
            self.status = Option(**self.status) # type: ignore
        if type(self.rich_text) == list:
            new_rich_text = []
            for _,rich_text in enumerate(self.rich_text):
                if type(rich_text) == dict:
                    new_rich_text.append(RichText(**rich_text)) # type: ignore
                else:
                    new_rich_text.append(rich_text)
            self.rich_text = new_rich_text
        super().__post_init__() 
        
    def __zip(self) -> dict: 
        return dict(zip(ALL_PROPERTIES_TYPES,
                        [self.title, self.rich_text, self.number, self.select, 
                        self.multi_select, self.status, self.date, self.people, 
                        self.files, self.checkbox, self.url, self.email, 
                        self.phone_number, self.relation, self.formula, 
                        self.rollup, self.created_time, self.created_by, 
                        self.last_edited_time, self.last_edited_by,
                        ]))

    def asdict(self) -> dict: 
        _zip_value = self.__zip()
        if (type(_zip_value[self.type]) == dict or
            type(_zip_value[self.type]) == str or
            type(_zip_value[self.type]) == int or
            type(_zip_value[self.type]) == float or
            type(_zip_value[self.type]) == bool or
            _zip_value[self.type] == None):
            value = _zip_value[self.type]
        elif type(_zip_value[self.type]) == list:
            value = [ _ if type(_) == dict else _.asdict()
                     for _ in _zip_value[self.type]]
        else:
            value = _zip_value[self.type].asdict()
        
        if (type(value) == dict and 
            ('options' in value or 'groups' in value)):
                for _, options in value.items(): # type: ignore
                    for option in options:
                        clear_empty_id(option)

        Dict = {
                "id": self.id,
                self.type: value,
                "type": self.type,
                }
        if self.type == 'relation':
            Dict['has_more'] = self.has_more
        
        clear_empty_id(Dict)
        return Dict

    def get_value(self):
        return self.Dict[self.type]

#--------------------------[Page]---------------------#
# FC: [Page] object
@dataclass
class Page(RequestInfo): 
    object: str = 'page'
    properties: dict[str, PropertyItem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        new_properties = {}
        if type(self.properties) == dict:
            for name, value in self.properties.items():
                new_properties.update({name: PropertyItem(**value)}) # type: ignore
        self.properties = new_properties
        super().__post_init__()
    
    def asdict(self) -> dict: 
        Dict = super().asdict()
            
        new_properties = {}
        for name, value in self.properties.items():
            if type(value) != dict:
                value = value.asdict()
            new_properties.update({name: value}) 
        Dict['properties'] = new_properties
        
        return Dict
    
    def update_title(self, title:RichText):
        for _, item in self.properties.items():
            if item.type == 'title':
                item.title = [title]
                break
        self.update()
        
    def update_item(self, name:str, **kwargs):
        old_item = self.properties[name].Dict
        self.properties[name] = PropertyItem(id=old_item['id'],
                                             type=old_item['type'],
                                             **kwargs)
        self.update()
    
    def clear_item(self, name:str):
        old_item = self.properties[name].Dict
        self.properties[name] = PropertyItem(id=old_item['id'],
                                             type=old_item['type'])
        self.update()
        
    def get_item(self, name:str) ->PropertyItem:
        return self.properties[name]
    
    def get_items(self) ->dict[str, dict[str, str]]:
        items = {}
        for name, item in self.properties.items():
            items.update({name: item.Dict})
        return items
    
    def property_list(self) ->list[dict]:
        property_dict = self.get_items()
        property_list = []
        for name, item in property_dict.items():
            property_list.append({"name":name, "item":item})
        return property_list
    
#--------------------------[Database]---------------------#
# FC: [Database] object
@dataclass
class Database(RequestInfo): 
    object: str = 'database'
    description: list[RichText] = field(default_factory=list)
    is_inline: bool = False
    properties: dict[str, PropertyType | None] = field(default_factory=dict)
    title: list[RichText] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        new_description = []
        for _, text in enumerate(self.description):
            if type(text) == dict:
                new_description.append(RichText(**text)) # type: ignore
        self.description = new_description
        
        if type(self.properties) == dict:
            new_properties = {}
            for name, value in self.properties.items():
                new_properties.update({name:PropertyType(**value)}) # type: ignore
            self.properties = new_properties
            
        new_title = []
        for _, text in enumerate(self.title):
            if type(text) == dict:
                new_title.append(RichText(**text)) # type: ignore
        self.title = new_title
        super().__post_init__()
        
    def asdict(self) -> dict:
        Dict = super().asdict()
        
        new_properties = {}
        for name, value in self.properties.items():
            if type(value) == dict or value is None:
                new_properties.update({name:value}) 
            else:
                new_properties.update({name:value.asdict()}) 
        Dict['properties'] = new_properties

        return Dict
    
    def update_title(self, title:RichText):
        self.title = [title]
        self.update()
        
    def update_property(self, name:str, **kwargs):
        property_type_object = self.properties[name]
        if property_type_object is not None:
            property_type = property_type_object.type
            self.properties[name] = PropertyType(name=name, type=property_type, **kwargs)
        else:
            self.properties[name] = PropertyType(name=name, **kwargs)
        self.update()
    
    def rename_property(self, old_name:str, new_name:str):
        self.properties[old_name].name = new_name # type: ignore
        self.update()

    def property_list(self) ->list[dict]:
        return [type_object.label_dict() if type_object is not None else None
                for _, type_object in self.properties.items()] # type: ignore
  
    def del_property(self, name:str):
        self.properties[name] = None
        self.update()
        
# FC: [Database] container object: paginated responses
@dataclass
class DatabaseContainer(BaseMethod):
    has_more: bool = False
    next_cursor: str | None = None
    object: str = 'list'
    page: dict = field(default_factory=dict)
    results: list[Page] = field(default_factory=list)
    type: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        new_pages = []
        for page in self.results:
            if type(page) == dict:
                new_pages.append(Page(**page)) # type: ignore
            else:
                new_pages.append(page)
        self.results = new_pages
        super().__post_init__()
        
    def asdict(self) -> dict:
        Dict = super().asdict()

        Dict['results'] = [page if type(page) == dict else page.asdict()
                            for page in self.results]
        return Dict

#--------------------------[Block]---------------------#
# FC: [Block] Retrieve request info
@dataclass
class Block(BlockBase, BaseMethod):
    type: str = field(default_factory=str)
    
    # text block
    paragraph: Paragraph = field(default_factory=Paragraph)
    heading_1: Heading = field(default_factory=Heading)
    heading_2: Heading = field(default_factory=Heading)
    heading_3: Heading = field(default_factory=Heading)
    callout: Callout = field(default_factory=Callout)
    quote: Quote = field(default_factory=Quote)
    bulleted_list_item: BulletedListItem = field(default_factory=BulletedListItem)
    numbered_list_item: NumberedListItem = field(default_factory=NumberedListItem)
    to_do: ToDo = field(default_factory=ToDo)
    toggle: Toggle = field(default_factory=Toggle)
    code: Code = field(default_factory=Code)
    # child page
    child_page: ChildPage = field(default_factory=ChildPage)
    child_database: ChildDatabase = field(default_factory=ChildDatabase)
    # Url block
    embed: Url = field(default_factory=Url)
    bookmark: Url = field(default_factory=Url)
    link_preview: Url = field(default_factory=Url)
    ## Media block
    image: FileLink = field(default_factory=FileLink)
    video: FileLink = field(default_factory=FileLink)
    pdf: FileLink = field(default_factory=FileLink)
    # Other
    equation: Expression = field(default_factory=Expression)
    divider: dict = field(default_factory=dict)
    table_of_contents: ColorMethod = field(default_factory=ColorMethod)
    breadcrumb: dict = field(default_factory=dict)
    template: Template = field(default_factory=Template)
    link_to_page: LinkTo = field(default_factory=LinkTo)
    synced_block: SyncedBlock = field(default_factory=SyncedBlock)
    ## column is column_list children.
    column_list: dict = field(default_factory=dict)
    column: dict = field(default_factory=dict)
    ## table_row is table children.
    table: Table = field(default_factory=Table)
    table_row: TableRow = field(default_factory=TableRow)
    
    def __post_init__(self) -> None:
        if not self.type in BLOCK_TYPE_LIST:
            raise ValueError(f"Block type {self.type} is not in the BLOCK_TYPE_LIST")
        
        self.paragraph = Paragraph(**self.paragraph) if type(self.paragraph) == dict else self.paragraph # type: ignore
        self.heading_1 = Heading(**self.heading_1) if type(self.heading_1) == dict else self.heading_1 # type: ignore
        self.heading_2 = Heading(**self.heading_2) if type(self.heading_2) == dict else self.heading_2 # type: ignore
        self.heading_3 = Heading(**self.heading_3) if type(self.heading_3) == dict else self.heading_3 # type: ignore
        self.callout = Callout(**self.callout) if type(self.callout) == dict else self.callout # type: ignore
        self.quote = Quote(**self.quote) if type(self.quote) == dict else self.quote # type: ignore
        self.bulleted_list_item = BulletedListItem(**self.bulleted_list_item) if type(self.bulleted_list_item) == dict else self.bulleted_list_item # type: ignore
        self.numbered_list_item = NumberedListItem(**self.numbered_list_item) if type(self.numbered_list_item) == dict else self.numbered_list_item # type: ignore
        self.to_do = ToDo(**self.to_do) if type(self.to_do) == dict else self.to_do # type: ignore
        self.toggle = Toggle(**self.toggle) if type(self.toggle) == dict else self.toggle # type: ignore
        self.code = Code(**self.code) if type(self.code) == dict else self.code # type: ignore
        self.child_page = ChildPage(**self.child_page) if type(self.child_page) == dict else self.child_page # type: ignore
        self.child_database = ChildDatabase(**self.child_database) if type(self.child_database) == dict else self.child_database # type: ignore
        self.embed = Url(**self.embed) if type(self.embed) == dict else self.embed # type: ignore
        self.bookmark = Url(**self.bookmark) if type(self.bookmark) == dict else self.bookmark # type: ignore
        self.link_preview = Url(**self.link_preview) if type(self.link_preview) == dict else self.link_preview # type: ignore
        self.image = FileLink(**self.image) if type(self.image) == dict else self.image # type: ignore
        self.video = FileLink(**self.video) if type(self.video) == dict else self.video # type: ignore
        self.pdf = FileLink(**self.pdf) if type(self.pdf) == dict else self.pdf # type: ignore
        self.equation = Expression(**self.equation) if type(self.equation) == dict else self.equation # type: ignore
        self.table_of_contents = ColorMethod(**self.table_of_contents) if type(self.table_of_contents) == dict else self.table_of_contents # type: ignore
        self.template = Template(**self.template) if type(self.template) == dict else self.template # type: ignore
        self.link_to_page = LinkTo(**self.link_to_page) if type(self.link_to_page) == dict else self.link_to_page # type: ignore
        self.synced_block = SyncedBlock(**self.synced_block) if type(self.synced_block) == dict else self.synced_block # type: ignore
        self.table = Table(**self.table) if type(self.table) == dict else self.table # type: ignore
        self.table_row = TableRow(**self.table_row) if type(self.table_row) == dict else self.table_row # type: ignore
        super().__post_init__()

    def __zip(self) -> dict:
        return dict(zip(BLOCK_TYPE_LIST,
                        [self.paragraph, self.heading_1, self.heading_2, self.heading_3,
                         self.callout, self.quote, self.bulleted_list_item, self.numbered_list_item,
                         self.to_do, self.toggle, self.code, self.child_page, self.child_database,
                         self.embed, self.bookmark, self.link_preview, self.image, self.video, self.pdf,
                         self.equation, self.divider, self.table_of_contents, self.breadcrumb, self.template, 
                         self.link_to_page, self.synced_block, self.column_list, self.column,
                         self.table, self.table_row]))
    
    def update(self) -> None:
        self.Dict = self.asdict()
   
    def asdict(self) -> dict:
        _zip_value = self.__zip()

        value = _zip_value[self.type].asdict() if _zip_value[self.type] != {} and type(_zip_value[self.type]) != dict else _zip_value[self.type]
        
        Dict = {
            "archived": self.archived,
            "created_by": self.created_by if type(self.created_by) == dict else self.created_by.asdict(),
            "created_time": self.created_time,
            "has_children": self.has_children,
            "id": self.id,
            "last_edited_by": self.last_edited_by if type(self.last_edited_by) == dict else self.last_edited_by.asdict(),
            "last_edited_time": self.last_edited_time,
            "object": self.object,
            "parent": self.parent if type(self.parent) == dict else self.parent.asdict(),
            "type": self.type,
            self.type: value,
        }

        return Dict

    def update_block(self, **kwargs):
        self.__init__(type=self.type,
                      id=self.id,
                      has_children=self.has_children,
                      archived=self.archived,
                      parent=self.parent,
                      **kwargs)
        self.__post_init__()
        
    def block_base_dict(self) -> dict:
        block_dict = self.Dict.copy()
        block_dict.pop('created_by')
        block_dict.pop('created_time')
        block_dict.pop('id')
        block_dict.pop('last_edited_by')
        block_dict.pop('last_edited_time')
        block_dict.pop('parent')
        return block_dict
    
    def block_item(self) -> dict:
        return {self.type: self.Dict[self.type]}
    
    def block_id_type(self) -> dict:
        return {
                "id":self.id,
                "type":self.type,
                }
        
# FC: [Block] children list
@dataclass
class BlockList(BaseMethod):
    """
    Raises:
        ValueError:  If the "type" is not in the BLOCK_CHILDREN_TYPES
    """
    block: dict = field(default_factory=dict)
    has_more: bool = False
    next_cursor: str | None = None
    object: str = 'list'
    results: list[Block] = field(default_factory=list)
    type: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if not self.type in BLOCK_CHILDREN_TYPES:
            raise ValueError(f'Invalid type: {self.type}')
        
        new_results = []
        for block in self.results:
            if type(block) == dict:
                new_results.append(Block(**block)) # type: ignore
            else:
                new_results.append(block)
        self.results = new_results
        super().__post_init__()
    
    def asdict(self) -> dict:
        Dict = super().asdict()
        
        new_results = []
        for block in self.results:
            if type(block) == dict:
                new_results.append(block)
            else:
                new_results.append(block.asdict())
        Dict['results'] = new_results
        return Dict
    
    def get_block(self, id: int) -> Block | None:
        for block in self.results:
            if block.id == id:
                return block
        return None
    
    def get_block_short_list(self) -> list[dict]:
        return [block.block_id_type() for block in self.results]
        