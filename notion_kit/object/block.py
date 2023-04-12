from dataclasses import dataclass, field

from .base import *
from .property_item import (
    RichText,
    Parent,
    Icon,
)
from ..CONTENTS import (
    TEXT_COLOR_LIST,
    CODE_LANGUAGE_LIST
)

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
