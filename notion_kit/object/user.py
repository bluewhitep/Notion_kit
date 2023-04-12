from dataclasses import dataclass, field

from .base import (
    BaseMethod,
)

# FC: [User] bot owner
@dataclass
class BotOwner(BaseMethod): 
    type: str = 'workspace'
    workspace: bool = True
    
# FC: [User] bot base
@dataclass
class BotBase(BaseMethod): 
    owner: BotOwner = field(default_factory=BotOwner)
    workspace_name: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if type(self.owner) == dict:
            self.owner = BotOwner(**self.owner) # type: ignore
        super().__post_init__()

# FC: [User] user short
@dataclass
class UserShort(BaseMethod): 
    id: str = field(default_factory=str)
    object: str = field(default_factory=str)