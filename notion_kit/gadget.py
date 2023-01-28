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
from pprint import pformat

from notion_kit import object
from notion_kit.dict_gadget import Dict_Gadget

class Debug:
    @staticmethod
    def fill_line(str_list:list, max_line:int, width:int=0) ->None:
        """
        Fill line with spaces

        Parameter
            str_list:       (list)      - list of string    
            max_line:       (int)       - max line
            width:          (int)       - width of each line. default 0
        """
        str_len = len(str_list)
        fill_count = max_line - str_len
        fill_line = "" if width == 0 else " "*width
        for _ in range(fill_count):
            str_list.append(fill_line)
    
    @staticmethod  
    def print_both(object1, object2, each_width=80, seq="#", grid:bool=False) ->None:
        """
        Print two object side by side
        
        Parameter
            object1:        (object)    - object 1
            object2:        (object)    - object 2
            each_width:     (int)       - pformat width. default 80
            seq:            (str)       - sequence between two object. default "#"
            grid:           (bool)      - show grid. default False
        """
        str1 = pformat(object1, width=each_width, sort_dicts=True).splitlines()
        str2 = pformat(object2, width=each_width, sort_dicts=True).splitlines()
        
        max_width = max([len(line) for line in str1]) + 1
        max_line = max(len(str1), len(str2))
        Debug.fill_line(str1, max_line, max_width)
        Debug.fill_line(str2, max_line)
        
        if grid:
            number="123456789|"*((max_width*2)//10 +1)
            number = number[:max_width*2+1]
            print(number + "| Total: " + str(len(number)))
            
        for i in range(max_line):
            filled_str1 = str1[i]+" "*(max_width - len(str1[i]))
            line = filled_str1 + seq + " " + str2[i]
            print(line)

    @staticmethod
    def print_diff(object1, object2, each_width=80, seq="#", grid:bool=False) ->None:
        """
        Print the difference
        
        Parameter
            object1:        (object)    - object 1
            object2:        (object)    - object 2
            each_width:     (int)       - pformat width. default 80
            seq:            (str)       - sequence between two object. default "#"
            grid:           (bool)      - show grid. default False
        """
        str1 = pformat(object1, width=each_width, sort_dicts=True).splitlines()
        str2 = pformat(object2, width=each_width, sort_dicts=True).splitlines()
        
        max_width = max([len(line) for line in str1]) + 1
        max_line = max(len(str1), len(str2))
        Debug.fill_line(str1, max_line, max_width)
        Debug.fill_line(str2, max_line)
        
        if grid:
            number="123456789|"*((max_width*2)//10 +1)
            number = number[:max_width*2+1]
            print(" |"+ number + "| Total: " + str(len(number)))
            
        for i in range(max_line):
            is_different = str1[i] != str2[i]
            BG_RED = '\033[41m'
            RESET = '\033[0m'
            marker = "-|"if is_different else " |" 
            filled_str1 = str1[i]+" "*(max_width - len(str1[i]))
            line = marker+ filled_str1 + seq + " " + str2[i]
            line = BG_RED + line + BG_RED if is_different else RESET + line + RESET
            print(line)

class Object:
    #-----------------------[Get object]-----------------------#
    # FC: [Date]
    @staticmethod
    def get_date(start:str, end:str | None = None) ->object.Date:
        """
        Get date
        
        Parameter
            start:              (str)       - start
            end:                (str)       - end
        
        Return
            object.Date
        """
        return object.Date(start=start, end=end)
    
    # FC: [File Link]
    @staticmethod
    def get_file_link(name:str, url:str) ->object.FileLink:
        """
        Get file link
        
        Parameter
            name:               (str)       - name
            url:                (object.Url) - url
        
        Return
            object.FileLink
        """
        return object.FileLink(name=name, external=object.Url(url=url))
    
    # FC: [File Upload]
    @staticmethod
    def get_file_upload(name:str, url:str, expiry_time:str) ->object.FileUpload:
        """
        Get file upload
        
        Parameter
            name:               (str)       - name
            url:                (object.Url) - url
        
        Return
            object.FileUpload
        """
        return object.FileUpload(name=name, 
                                 file=object.Upload(url=url, 
                                                    expiry_time=expiry_time))
        
    # FC: [Formula Value]
    @staticmethod
    def get_formula_value(type:str, 
                          string:str | None = None,
                          number:float | None = None,
                          boolean:bool = False,
                          date_start:str | None = None,
                          date_end:str | None = None) ->object.FormulaValue:
        """
        Get formula value
        
        Parameter
            type:               (str)       - type
            string:             (str)       - string
            number:             (float)     - number
            boolean:            (bool)      - boolean
            date_start:         (str)       - date start
            date_end:           (str)       - date end
            
        Return
            object.FormulaValue
        
        Raise
            ValueError      - date_start is required
            Invalid type    - type is invalid
        """
        if type == "string":
            return object.FormulaValue(type=type, string=string)
        elif type == "number":
            return object.FormulaValue(type=type, number=number)
        elif type == "boolean":
            return object.FormulaValue(type=type, boolean=boolean)
        elif type == "date":
            assert date_start is not None, "date_start is required"
            return object.FormulaValue(type=type, date=object.Date(start=date_start,
                                                                   end=date_end))
        else:
            raise ValueError("Invalid type")
        
    # FC: [Option]
    @staticmethod
    def get_option(name:str, color:str="default") ->object.Option:
        """
        Get option
        
        Parameter
            name:               (str)       - name
            color:              (str)       - color
        
        Return
            object.Option
        """
        return object.Option(name=name, color=color)
    
    # FC: [Rich Text]
    @staticmethod
    def get_rich_text(text:str = "",
                      link:str | None = None,
                      bold: bool = False,
                      italic: bool = False,
                      strikethrough: bool = False,
                      underline: bool = False,
                      code: bool = False,
                      color: str = "default") ->object.RichText:
        """
        Get rich text
        
        Parameter
            text:               (str)       - text
            link:               (str)       - link
            bold:               (bool)      - bold
            italic:             (bool)      - italic
            strikethrough:      (bool)      - strikethrough
            underline:          (bool)      - underline
            code:               (bool)      - code
            color:              (str)       - color
        
        Return
            object.RichText
        """
        url = object.Url(url=link) if link is not None else None
        text_content = object.TextContent(content=text,
                                          link=url)
        text_style = object.TextStyle(bold, italic, strikethrough,
                                      underline, code, color)
        
        return object.RichText(text=text_content, annotations=text_style)
    
    # FC: [Hyperlink Rich Text]
    @staticmethod
    def get_hyperlink(text:str,
                      link:str,
                      bold: bool = False,
                      italic: bool = False,
                      strikethrough: bool = False,
                      underline: bool = False,
                      code: bool = False,
                      color: str = "default") ->object.RichText:
        """
        Get rich text
        
        Parameter
            text:               (str)       - text
            link:               (str)       - link
            bold:               (bool)      - bold
            italic:             (bool)      - italic
            strikethrough:      (bool)      - strikethrough
            underline:          (bool)      - underline
            code:               (bool)      - code
            color:              (str)       - color
        
        Return
            object.RichText
        """
        url = object.Url(url=link)
        text_content = object.TextContent(content=text,
                                          link=url)
        text_style = object.TextStyle(bold, italic, strikethrough,
                                      underline, code, color)
        
        return object.RichText(text=text_content, annotations=text_style)
    
    # FC: [Rollup Item]
    @staticmethod
    def get_rollup_item(type:str,
                        function:str,
                        number:int = 0,
                        date_start:str | None = None,
                        date_end:str | None = None,
                        array: list[dict] = [],
                        incomplete: dict = {}) -> object.RollupItem:
        """
        Get rollup item
        
        Parameter
            type:               (str)       - type
            function:           (str)       - function
            number:             (int)       - number
            data_start:         (str)       - data start
            data_end:           (str)       - data end
            array:              (list)      - array
            incomplete:         (dict)      - incomplete
            
        Return
            object.RollupItem
            
        Raise
            ValueError      - type is invalid
            ValueError      - date_start is required
        """
        if type == "number":
            return object.RollupItem(type=type, function=function,
                                     number=number)
        elif type == "date":
            assert date_start is not None, "date_start is required"
            return object.RollupItem(type=type, function=function,
                                     date=object.Date(start=date_start,
                                                      end=date_end))
        elif type == "array":
            return object.RollupItem(type=type, function=function,
                                     array=array)
        elif type == "incomplete":
            return object.RollupItem(type=type, function=function,
                                     incomplete=incomplete)
        else:
            raise ValueError("Invalid type")

class PropertyType:
    #-----------------------[Property Type]-----------------------#
    # FC: [Generic Property Type]
    @staticmethod
    def get(name:str, type:str) ->object.PropertyType:
        """
        Get property type
        
        Parameter
            name:       (str)       - name
            type:       (str)       - type
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type=type)
    
    # FC: [Rich text]
    @staticmethod
    def get_rich_text(name:str) ->object.PropertyType:
        """
        Get rich text property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='rich_text')
    
    # FC: [Number]
    @staticmethod
    def get_number(name:str, format:str='number') ->object.PropertyType:
        """
        Get number property type
        
        Parameter
            name:       (str)       - name
            format:     (str)       - format. default "number"
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='number', 
                                   number=object.Number(format=format))
    
    # FC: [Select]
    @staticmethod
    def get_select(name:str, options:list[object.Option]) ->object.PropertyType:
        """
        Get select property type
        
        Parameter
            name:       (str)       - name
            options:    (list[object.Option]) - options
            
        Return
            object.PropertyType
            
        Raise
            AssertionError - options must be list of object.Option
        """
        for option in options:
            assert type(option) == object.Option, "options must be list of object.Option"
        return object.PropertyType(name=name, type='select', 
                                   select=object.Options(options=options))
    
    # FC: [Multi-select]
    @staticmethod
    def get_multi_select(name:str, options:list[object.Option]) ->object.PropertyType:
        """
        Get multi-select property type
        
        Parameter
            name:       (str)       - name
            options:    (list[object.Option]) - options
            
        Return
            object.PropertyType
            
        Raise
            AssertionError - options must be list of object.Option
        """
        for option in options:
            assert type(option) == object.Option, "options must be list of object.Option"
        return object.PropertyType(name=name, type='multi_select', 
                                   multi_select=object.Options(options=options))
        
    # FC: [Date]
    @staticmethod
    def get_date(name:str) ->object.PropertyType:
        """
        Get date property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='date')
    
    # FC: [People]
    @staticmethod
    def get_people(name:str) ->object.PropertyType:
        """
        Get people property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='people')
    
    # FC: [Files]
    @staticmethod
    def get_files(name:str) ->object.PropertyType:
        """
        Get files property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='files')
    
    # FC: [Checkbox]
    @staticmethod
    def get_checkbox(name:str) ->object.PropertyType:
        """
        Get checkbox property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='checkbox')
    
    # FC: [Url]
    @staticmethod
    def get_url(name:str) ->object.PropertyType:
        """
        Get url property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='url')
    
    # FC: [Email]
    @staticmethod
    def get_email(name:str) ->object.PropertyType:
        """
        Get email property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='email')
    
    # FC: [Phone Number]
    @staticmethod
    def get_phone_number(name:str) ->object.PropertyType:
        """
        Get phone number property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='phone_number')
    
    # FC: [Relation Single]
    @staticmethod
    def get_relation_single(name:str, database_id:str) ->object.PropertyType:
        """
        Get relation single property type
        
        Parameter
            name:           (str)       - name
            database_id:    (str)       - database id
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='relation', 
                                   relation=object.RelationSingle(database_id=database_id))
    
    # FC: [Relation Dual]
    @staticmethod
    def get_relation_dual(name:str, database_id:str,
                                    synced_id:str,
                                    synced_name:str) ->object.PropertyType:
        """
        Get relation dual property type
        
        Parameter
            name:           (str)       - name
            database_id:    (str)       - database id
            
        Return
            object.PropertyType
        """
        dual_property = object.RelationSynced(synced_property_id=synced_id,
                                             synced_property_name=synced_name)
        relation_dual = object.RelationDual(database_id=database_id,
                                            dual_property=dual_property)
        return object.PropertyType(name=name, type='relation', 
                                   relation=relation_dual)
    
    # FC: [Formula]
    @staticmethod
    def get_formula(name:str, expression:str="") ->object.PropertyType:
        """
        Get formula property type
        
        Parameter
            name:           (str)       - name
            expression:     (str)       - expression
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='formula', 
                                   formula=object.Formula(expression=expression))
    
    # FC: [Created Time]
    @staticmethod
    def get_created_time(name:str) ->object.PropertyType:
        """
        Get created time property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='created_time')
    
    # FC: [Created By]
    @staticmethod
    def get_created_by(name:str) ->object.PropertyType:
        """
        Get created by property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='created_by')
    
    # FC: [Last Edited Time]
    @staticmethod
    def get_last_edited_time(name:str) ->object.PropertyType:
        """
        Get last edited time property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='last_edited_time')
    
    # FC: [Last Edited By]
    @staticmethod
    def get_last_edited_by(name:str) ->object.PropertyType:
        """
        Get last edited by property type
        
        Parameter
            name:       (str)       - name
            
        Return
            object.PropertyType
        """
        return object.PropertyType(name=name, type='last_edited_by')
    
    # FC: [Delete]
    @staticmethod
    def delete(name:str) ->dict:
        """
        Get delete property type
        
        Parameter
            name:       (str)       - name
            
        Return
            dict
        """
        return {name: None}
    
    # FC: [Rename]
    @staticmethod
    def rename(old_name:str, new_name:str) ->dict:
        """
        Get rename property type
        
        Parameter
            old_name:   (str)       - old name
            new_name:   (str)       - new name
            
        Return
            dict
        """
        return {old_name: {"name":new_name}}
    
class PropertyItem:
    #-----------------------[Property Item]-----------------------#
    pass

class Block:
    #-----------------------[Block]-----------------------#
    # FUNTURE: [Get block tree]
    pass

class Gadget:
    Debug = Debug()
    Object = Object()
    PropertyType = PropertyType()
    # PropertyItem = PropertyItem()
    # Block = Block()
    Dict = Dict_Gadget()
    
    #-----------------------[Database]-----------------------#
    # FC: [Update database property]
    @staticmethod
    def update_database_property(database_object:object.Database,
                                 property_name:str,
                                 new_property:object.PropertyType) ->object.Database:
        """
        Update database property
        
        Parameter
            database_object:    (object.Database)       - database object
            property_name:      (str)                   - property name
            new_property:       (object.PropertyType)   - new property
            
        Return
            object.Database [option]
        """
        new_property.type = database_object.properties[property_name].type # type: ignore
        new_property.id = database_object.properties[property_name].id # type: ignore
        new_property.name = database_object.properties[property_name].name # type: ignore
        database_object.properties[property_name] = new_property
        database_object.update()
        return database_object
    
    # FC: [Update database title]
    @staticmethod
    def update_database_title(database_object:object.Database,
                              **kwargs) ->object.Database:
        """
        Update database title
        
        Parameter
            database_object:    (object.Database)       - database object
            kwargs:             (dict)                  - kwargs
            
        Return
            object.Database [option]
        """
        rich_text = Object.get_rich_text(**kwargs)
        database_object.update_title(rich_text)
        return database_object
    
    # FC: [Update database icon]
    @staticmethod
    def update_database_icon(database_object:object.Database,
                            emoji:str) ->object.Database:  
        """
        Update database icon
        
        Parameter
            database_object:    (object.Database)       - database object
            icon:                (str)                   - icon
            
        Return
            object.Database [option]
        """
        database_object.icon = object.Icon(emoji=emoji)
        return database_object
        
    # FC: [Rename database property]
    @staticmethod
    def rename_database_property(database_object:object.Database,
                                 old_name:str,
                                 new_name:str) ->object.Database:
        """
        Rename database property
        
        Parameter
            database_object:    (object.Database)       - database object
            old_name:            (str)                   - old name
            new_name:            (str)                   - new name
            
        Return
            object.Database [option]
        """
        database_object.rename_property(old_name, new_name)
        return database_object
    
    # FC: [Delete database property]
    @staticmethod
    def del_database_property(database_object:object.Database,
                                property_name:str) ->object.Database:
        """
        Delete database property
        
        Parameter
            database_object:    (object.Database)       - database object
            property_name:      (str)                   - property name
            
        Return
            object.Database [option]
        """
        database_object.del_property(property_name)
        return database_object
    
    #-----------------------[Page]-----------------------#
    # FC: [Update page property item]
    @staticmethod
    def update_page_property(page_object:object.Page,
                             property_name:str,
                             **kwargs) ->object.Page:
        """
        Update page property
        
        Parameter
            page_object:    (object.Page)           - page object
            property_name:      (str)                   - property name
            new_property:       (object.PropertyItem)   - new property
            
        Return
            object.Page [option]
        """
        new_property = object.PropertyItem(id=page_object.properties[property_name].id,
                                           type=page_object.properties[property_name].type,
                                           **kwargs)
        page_object.properties[property_name] = new_property
        page_object.update()
        return page_object
    
    # FC: [Update page title]
    @staticmethod
    def update_page_title(page_object:object.Page,
                          **kwargs) ->object.Page:
        """
        Update page title
        
        Parameter
            page_object:    (object.Page)           - page object
            kwargs:             (dict)                  - kwargs
            
        Return
            object.Page [option]
        """
        rich_text = Object.get_rich_text(**kwargs)
        page_object.update_title(rich_text)
        return page_object
    
    # FC: [Upadate page icon]
    @staticmethod
    def update_page_icon(page_object:object.Page,
                         emoji:str) ->object.Page:
        """
        Update page icon
        
        Parameter
            page_object:    (object.Page)           - page object
            icon:                (str)                   - icon
            
        Return
            object.Page [option]
        """
        page_object.icon = object.Icon(emoji=emoji)
        return page_object
    
    # FC: [Clear page property]
    @staticmethod
    def clear_page_property(page_object:object.Page,
                            property_name:str) ->object.Page:
        """
        Clear page property
        
        Parameter
            page_object:    (object.Page)           - page object
            property_name:      (str)                   - property name
            
        Return
            object.Page [option]
        """
        page_object.clear_item(property_name)
        return page_object
