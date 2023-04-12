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
from notion_kit import object 
from notion_kit.object import property_item 
from notion_kit.object import property_type

from notion_kit.CONTENTS import (
                        NON_CREATEABLE_PROPERTIES_TYPES,
                        NON_UPDATABLE_PROPERTIES_TYPES,
                        NON_UPDATABLE_PROPERTIES_ITEMS,
                        )

class BaseAPI:
    def __init__(self, client, id:str | None):
        self.id = id
        self.client = client

class Page(BaseAPI):
    def __init__(self, client, id:str | None):
        super().__init__(client, id)
   
    def create_in_database(self,
                           parent_database_id:str,
                           title:str | property_item.RichText | None,
                           properties_item_dict:dict[str,object.PropertyItem] | None = None,
                           icon:str | property_item.Icon | None = None,
                           cover:str | property_item.Url | None = None
                           #children:list[property_item.Block] | None = None
                           ) ->object.Page:
        """
        Create page in database
        
        Parameters:
            parent_database_id:        (str)                           - Target database id
            title:                     (property_item.RichText)        - New page title
            properties_item_dict       (dict[str,object.PropertyItem]) - 
            icon:                      (property_item.Icon)            - New page icon [Optional]
            cover:                     (property_item.FileLink)        - New page cover [Optional]
            children:                  (list[property_item.Block])     - New page children [unavailable]
            
        Returns:
            object.Page:               (object.Page)                   - New page
        """
        if type(title)==str:
            title = property_item.RichText(text=title)

        kwargs = {
            'parent': property_item.Parent(type="database_id", database_id=parent_database_id).Dict,
            'properties': {"Name": {"title": [title.Dict]}}
            }
        
        if properties_item_dict is not None:
            for name, properties in properties_item_dict.items():
                if properties.type in NON_UPDATABLE_PROPERTIES_ITEMS:
                    continue
                else:
                    kwargs['properties'].update({name: properties.Dict})
                    
        if icon is not None:
            kwargs['icon'] = icon.Dict
        if cover is not None:
            kwargs['cover'] = cover.Dict
        return object.Page(**self.client.pages.create(**kwargs))
   
    def create_in_page(self, 
                       parent_page_id, 
                       title:property_item.RichText | None = None, 
                       icon:property_item.Icon | None = None, 
                       cover:property_item.FileLink | None = None, 
                       # children:list[object.Block] | None = None 
                       ) ->object.Page:
        """
        Create page in database
        
        Parameters:
            parent_page_id:            (str)                    - Target database id
            title:                     (property_item.RichText)        - New page title
            icon:                      (property_item.Icon)            - New page icon [Optional]
            cover:                     (property_item.FileLink)        - New page cover [Optional]
            children:                  (list[object.Block])     - New page children [unavailable]
            
        Returns:
            object.Page:               (object.Page)            - New page
        """
        kwargs = {
            'parent': property_item.Parent(type="page_id", page_id=parent_page_id).Dict, # type: ignore
            'properties': {"title": [title.Dict]}, # type: ignore
            }
        if icon is not None:
            kwargs['icon'] = icon.Dict
        if cover is not None:
            kwargs['cover'] = cover.Dict
        return object.Page(**self.client.pages.create(**kwargs))
     
    def get_data(self, page_id:str) ->object.Page:
        """
        Use notion client api get page info dict

        Parameters:
            page_id:            (str)            - Target page id
            
        Return:
            object.Page:        (object.Page)    - Target page information
        """   
        return object.Page(**self.client.pages.retrieve(page_id))
    
    def update(self, new_page_object:object.Page) ->object.Page:
        """
        Update page 

        Parameters:
            new_page_object:        (object.Page)       - Will update dict of properties
            
        Return:
            object.Page:            (object.Page)       - New page dict
        """
        page_dict = new_page_object.Dict
        for name, value in page_dict['properties'].items():
            if value is None:
                continue
            if value['type'] in NON_UPDATABLE_PROPERTIES_ITEMS:
                new_page_object.properties.pop(name)
        new_page_object.update()
        
        return object.Page(**self.client.pages.update(new_page_object.id, 
                                                      **new_page_object.Dict))
    
class Database(BaseAPI):
    def __init__(self, client, id:str | None):
        super().__init__(client, id)
        
    def create(self, parent_page_id:str, 
                title:property_item.RichText,
                properties_type_list:list[object.PropertyType] | None = None,
                icon:property_item.Icon | None = None,
                cover:property_item.FileLink | None = None,
                is_inline:bool = False) ->object.Database:
        """
        Create database
    
        Parameters:
            parent_page_id:            (str)                       - Target database id
            title:                     (property_item.RichText)           - New database title
            properties_type:           (object.PropertyType)       - New database properties type [Optional]
            icon:                      (property_item.Icon)               - New database icon [Optional]
            cover:                     (property_item.FileLink)           - New database cover [Optional]
            is_inline:                 (bool)                      - New database inline [Optional]
                
        Return:
            object.Database:           (object.Database)           - New database
        """
        
        kwargs = {
            'parent': property_item.Parent(page_id=parent_page_id, type='page_id').asdict(),
            'title': [title.Dict],
            'properties': {"Name": {"title": {}}}
        }

        if properties_type_list is not None:
            for properties in properties_type_list:
                if properties.type in NON_CREATEABLE_PROPERTIES_TYPES:
                    continue
                else:
                    kwargs['properties'].update(properties.full_dict())
        if icon is not None:
            kwargs['icon'] = icon.Dict
        if cover is not None:
            kwargs['cover'] = cover.Dict
        if is_inline:
            kwargs['is_inline'] = is_inline
        return object.Database(**self.client.databases.create(**kwargs))
    
    def get_pages(self, database_id:str) ->object.DatabaseContainer:
        """
        Get database information

        Parameters:
            database_id:                (str)                       - Target database id
        
        Returns:
            object.DatabaseContainer:  (object.DatabaseContainer)   - Page information of database
        """
        return object.DatabaseContainer(**self.client.databases.query(database_id))

    def get_data(self, database_id:str) ->object.Database:
        """
        Get database information

        Parameters:
            database_id:        (str)       - Target database id

        Returns:
            object.Database:    (object.Database)   - Database information
        """
        return object.Database(**self.client.databases.retrieve(database_id))
        
    def update(self, new_database_object:object.Database) ->object.Database:
        """
        Update database 

        Parameters:
            new_database_object:        (object.Database)       - Will update dict of properties
            
        Return:
            object.Database:            (object.Database)       - New database dict
        """
        database_dict = new_database_object.Dict
        for name, value in database_dict['properties'].items():
            if value is None:
                continue
            if value['type'] in NON_UPDATABLE_PROPERTIES_TYPES:
                new_database_object.properties.pop(name)
        new_database_object.update()
        
        return object.Database(**self.client.databases.update(new_database_object.id, 
                                                              **new_database_object.Dict))
    
class User(BaseAPI):
    def __dict_to_object(self, user_dict:dict) ->object.User | object.Bot | None:
        """
        Convert dict to object
        
        Parameters:
            user_dict:      (dict)                      - User dict
            
        Returns:
            user_object:    (object_class.User | object_class.Bot)  - User object
        """
        if user_dict['type'] == 'person':
            return object.User(**user_dict)
        elif user_dict['type'] == 'bot':
            return object.Bot(**user_dict)
        return None

    def get_user_list(self) ->list[object.User | object.Bot]:
        """
        Get user list

        Returns:
            user_list:      (list)      - User list
        """
        user_list = self.client.users.list()['results']
        for i, user in enumerate(user_list):
            user_list[i] = self.__dict_to_object(user)
        return user_list
    
    def get_user_data(self, user_id:str) ->object.User | object.Bot | None:
        """
        Get user data

        Parameters:
            user_id:        (str)                               - Target user id

        Returns:
            user_data:      (object_class.User | object_class.Bot | None)   - User data [None if user not found]
        """
        return  self.__dict_to_object(self.client.users.retrieve(user_id=user_id))
    
    def who_am_i(self) ->object.Bot:
        """
        Get api user
        Who am I?

        Returns:
            object_class.Bot:     (object_class.Bot)    - Api user
        """
        return object.Bot(**self.client.users.me())

class Block(BaseAPI):
    def get_data(self, id:str) ->object.Block:
        """
        Get block data

        Parameters:
            block_id:           (str)                   - Target block id or page id
            
        Returns:
            object.Block:       (object.Block)          - Block data
        """
        return object.Block(**self.client.blocks.retrieve(block_id=id))
    
    def get_children_blocks(self, id:str) ->object.BlockList:
        """
        Get block childrens

        Parameters:
            block_id:           (str)                   - Target block id or page id
        
        Returns:
            property_item.BlockList:   (property_item.BlockList)      - Block childrens
        """
        return object.BlockList(**self.client.blocks.children.list(block_id=id))
    
    def add_block(self, id:str, block_list:list) ->object.BlockList:
        """
        Append block childrens

        Parameters:
            page_id:       (str)       - Target page id
            block_list:     (list)      - Will append block list

        Returns:
            childrens:      (dict)      - Childrens list
        """
        block_list = [block if type(block) == dict else block.block_base_dict()
                      for block in block_list]
        return object.BlockList(**self.client.blocks.children.append(block_id=id,
                                                                    children=block_list))
    
    def update(self, new_block_object: object.Block) ->object.Block:
        """
        Update block childrens

        Parameters:
            page_id:          (str)           - Target page id
            block_list:       (dict)          - Will update block list

        Returns:
            new_block_dict:      (dict)       - New block dict
        """
        return object.Block(**self.client.blocks.update(block_id=new_block_object.id,
                                                        **new_block_object.block_item()))
    
    def del_block(self, block_id:str) ->object.Block:
        """
        Delete block childrens

        Parameters:
            block_id:       (str)       - Target block id

        Returns:
            deleted_block: (dict)      - New block dict
        """
        return object.Block(**self.client.blocks.delete(block_id=block_id))
