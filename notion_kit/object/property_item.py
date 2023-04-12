from dataclasses import dataclass, field

from .base import *

from ..CONTENTS import (
    ROLLUP_FUNCTION_LIST,
    ROLLUP_TYPE_LIST,
)

#--------------------------[Base]---------------------#
# FC: Email
@dataclass
class Email(BaseMethod): 
    email: str = field(default_factory=str)
    
    def set_email(self, email: str) -> None:
        self.email = email
        super().asdict()

# FC: Url
@dataclass
class Url(BaseMethod): 
    url: str = field(default_factory=str)
    
    def set_url(self, url: str) -> None:
        self.url = url
        super().asdict()

# FC: Icon
@dataclass
class Icon(BaseMethod): 
    type: str = 'emoji'
    emoji: str = field(default_factory=str)
    
    def set_emoji(self, emoji: str) -> None:
        self.emoji = emoji
        super().asdict()

# FC: Date
@dataclass
class Date(BaseMethod): 
    start: str = field(default_factory=str)
    end: str | None = field(default_factory=str)
    time_zone: None = None
    
    def set_start(self, start: str) -> None:
        self.start = start
        super().asdict()
        
    def set_end(self, end: str) -> None:
        self.end = end
        super().asdict()

# FC: Mention
@dataclass
class Mention(BaseMethod): 
    type: str = field(default_factory=str)
    page: ID = field(default_factory=ID)
    database: ID = field(default_factory=ID)
    
    def __post_init__(self) -> None:
        if type(self.page) == dict:
            self.page = ID(**self.page)
        if type(self.database) == dict:
            self.database = ID(**self.database)
        super().__post_init__()
    
    def asdict(self) -> dict:
        Dict = super().asdict()
        if Dict['type'] == 'page':
            Dict.pop('database')
        elif Dict['type'] == 'database':
            Dict.pop('page')
        return Dict
    
    def set_page_id(self, page_id: str | ID) -> None:
        page_id_type = type(page_id)
        if page_id_type == str:
            self.page = ID(id=page_id)
        elif page_id_type == ID:
            self.page = page_id
        else:
            raise TypeError(f"page_id must be str or ID, not {page_id_type}")
        self.type = 'page'
        super().asdict()
        
    def set_database_id(self, database_id: str | ID) -> None:
        database_id_type = type(database_id)
        if database_id_type == str:
            self.database = ID(id=database_id)
        elif database_id_type == ID:
            self.database = database_id
        else:
            raise TypeError(f"database_id must be str or ID, not {database_id_type}")
        self.type = 'database'
        super().asdict()
    
    def get_id(self) -> str:
        if self.type == 'page':
            return self.page.id
        elif self.type == 'database':
            return self.database.id
        else:
            raise ValueError(f"Type {self.type} is not in ['page', 'database']")

# FC: Parent
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
    
    def set_page_id(self, page_id: str) -> None:
        self.page_id = page_id
        self.type = 'page_id'
        super().asdict()
        
    def set_database_id(self, database_id: str) -> None:
        self.database_id = database_id
        self.type = 'database_id'
        super().asdict()

    def get_id(self) -> str:
        if self.type == 'page_id':
            return self.page_id
        elif self.type == 'database_id':
            return self.database_id
        else:
            raise ValueError(f"Type {self.type} is not in ['page_id', 'database_id']")

#--------------------------[Formula]---------------------#
# FC: Formula value
@dataclass
class FormulaValue(BaseMethod): 
    """
    FormulaValue
    
    Parameters:
    ----------
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
            self.date = Date(**self.date)
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
        
    def set_string(self, string: str) -> None:
        self.type = 'string'
        self.string = string
        self.number = None
        self.boolean = False
        self.date = None
        super().asdict()
    
    def set_number(self, number: float) -> None:
        self.type = 'number'
        self.number = number
        self.string = None
        self.boolean = False
        self.date = None
        super().asdict()
    
    def set_boolean(self, boolean: bool) -> None:
        self.type = 'boolean'
        self.boolean = boolean
        self.string = None
        self.number = None
        self.date = None
        super().asdict()
        
    def set_date(self, date: Date) -> None:
        self.type = 'date'
        self.date = date
        self.string = None
        self.number = None
        self.boolean = False
        super().asdict()

#--------------------------[Rollup]---------------------#
# FC: Rollup item
@dataclass
class RollupItem(BaseMethod): 
    """
    RollupItem
    
    Parameters:
    ----------
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
            self.date = Date(**self.date)
        
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
   
#--------------------------[File]---------------------#
# FC: [file] upload
@dataclass
class Upload(BaseMethod): 
    url: str = field(default_factory=str)
    expiry_time: str = field(default_factory=str)
    
    def set_url(self, url: str) -> None:
        self.url = url
        super().asdict()

    def set_expiry_time(self, expiry_time: str) -> None:
        self.expiry_time = expiry_time
        super().asdict()
    
# FC: [file] object
@dataclass
class FileUpload(BaseMethod): 
    type: str = 'file'
    file: Upload = field(default_factory=Upload)
    name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.file) == dict:
            self.file = Upload(**self.file)
        super().__post_init__()
        
    def set_name(self, name: str) -> None:
        self.name = name
        super().asdict()
    
    def set_file(self, file: Upload | dict) -> None:
        file_of_type = type(file)
        if file_of_type == dict:
            self.file = Upload(**file)
        elif file_of_type == Upload:
            self.file = file
        else:
            raise ValueError(f"file must be either dict or Upload, not {file_of_type}")
        super().asdict()

# FC: [file] object
@dataclass
class FileLink(BaseMethod): 
    type: str = 'external'
    external: Url = field(default_factory=Url)
    name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        self.external = Url(**self.external) if type(self.external) == dict else self.external
        super().__post_init__()

    def set_name(self, name: str) -> None:
        self.name = name
        super().asdict()
    
    def set_external(self, external: Url | dict) -> None:
        external_of_type = type(external)
        if external_of_type == dict:
            self.external = Url(**external)
        elif external_of_type == Url:
            self.external = external
        else:
            raise ValueError(f"external must be either dict or Url, not {external_of_type}")
        super().asdict()
        
#--------------------------[Rich Text]---------------------#
# FC: [Text] content
@dataclass
class TextContent(BaseMethod): 
    content: str = field(default_factory=str)
    link: Url | None = None
    
    def __post_init__(self) -> None:
        if type(self.link) == dict:
            self.link = Url(**self.link)
        super().__post_init__()
    
    def text_dict(self, name:str="text") -> dict:
        return {name: self.asdict()}
    
    def set_text(self, text:str) -> None:
        self.content = text
        super().asdict()
    
    def set_link(self, link:str | Url) -> None:
        if type(link) == str:
            self.link = Url(url=link)
        super().asdict()
               
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
    
    def set_bold(self, bold:bool) -> None:
        self.bold = bold
        super().asdict()
    
    def set_italic(self, italic:bool) -> None:
        self.italic = italic
        super().asdict()
    
    def set_strikethrough(self, strikethrough:bool) -> None:
        self.strikethrough = strikethrough
        super().asdict()
    
    def set_underline(self, underline:bool) -> None:
        self.underline = underline
        super().asdict()
    
    def set_code(self, code:bool) -> None:
        self.code = code
        super().asdict()
    
    def set_color(self, color:str) -> None:
        check_color(color)
        self.color = color
        super().asdict()
    
    def set_stytle(self, 
                   bold:bool | None = None,
                   italic:bool | None = None,
                   strikethrough:bool | None = None,
                   underline:bool | None = None, 
                   code:bool | None = None, 
                   color:str | None = None) -> None:
        if bold is not None:
            self.set_bold(bold)
        if italic is not None:
            self.set_italic(italic)
        if strikethrough is not None:
            self.set_strikethrough(strikethrough)
        if underline is not None:
            self.set_underline(underline)
        if code is not None:
            self.set_code(code)
        if color is not None:
            self.set_color(color)
        super().asdict()
            
# FC: [Text] object
@dataclass
class RichText(BaseMethod): 
    type: str = "text" # or mention
    text: TextContent = field(default_factory=TextContent)
    mention: Mention | None = None
    annotations: TextStyle = field(default_factory=TextStyle)
    href: str | None = None
    plain_text: str | None = None
    
    def __post_init__(self) -> None:
        self.text = TextContent(**self.text) if type(self.text) == dict else self.text
        self.mention = Mention(**self.mention) if type(self.mention) == dict else self.mention
        self.plain_text = self.text.content
        if self.type == "text":
            self.href = self.text.link.url if self.text.link is not None else None
        elif self.type == "mention":
            self.href = 'https://www.notion.so/' + self.mention.get_id().replace('-', '')
        
        self.annotations = TextStyle(**self.annotations) if type(self.annotations) == dict else self.annotations
        super().__post_init__()
    
    def asdict(self) -> dict:
        Dict = super().asdict()
        if self.type == "text":
            Dict.pop("mention")
        elif self.type == "mention":
            Dict.pop("text")
        return Dict
    
    def set_text(self, text:str | dict | TextContent) -> None:
        type_of_text = type(text)
        if type_of_text == str:
            self.text.set_text(text)
        elif type_of_text == dict:
            self.text = TextContent(**text)
        elif type_of_text == TextContent:
            self.text = text
        else:
            raise TypeError(f"Type {type_of_text} is not supported")
        self.type = "text"
        super().asdict()
    
    def set_stytle(self, 
                   bold:bool | None = None,
                   italic:bool | None = None,
                   strikethrough:bool | None = None,
                   underline:bool | None = None, 
                   code:bool | None = None, 
                   color:str | None = None) -> None:
        self.annotations.set_stytle(bold, italic, strikethrough, underline, code, color)
        super().asdict()
    
    def set_hyperlink(self,
                      text:str | dict | TextContent,
                      link:str | Url) -> None:
        self.set_text(text)
        if type(link) == str:
            link = Url(url=link)
            self.text.set_link(link)
        elif type(link) == Url:
            self.text.set_link(link)
        else:
            raise TypeError(f"Type {type(link)} is not supported")
        super().asdict()
    
    def set_mention(self,
                    mention:dict | Mention) -> None:
        if type(mention) == dict:
            self.mention = Mention(**mention)
        elif type(mention) == Mention:
            self.mention = mention
        else:
            raise TypeError(f"Type {type(mention)} is not supported")
        self.type = "mention"
        super().asdict()

#--------------------------[Select \ Multi-Select \ Status]---------------------#
# FC: Option
@dataclass
class Option(BaseMethod): 
    id: str | None = field(default_factory=str)
    name: str = field(default_factory=str)
    color: str = field(default_factory=str)
    
    def set_name(self, name: str) -> None:
        self.name = name
        super().asdict()
    
    def set_color(self, color: str) -> None:
        self.color = color
        super().asdict()
    
# FC: Group
@dataclass
class Group(BaseMethod): 
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    color: str = field(default_factory=str)
    option_ids: list[str] = field(default_factory=list)
    
    def set_name(self, name: str) -> None:
        self.name = name
        super().asdict()
    
    def set_color(self, color: str) -> None:
        self.color = color
        super().asdict()
    
    def empty_option_ids(self) -> None:
        self.option_ids = []
        super().asdict()
