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
import sys
import time, datetime, pytz

from typing import Any
from notion_client.helpers import get_id, is_full_page, is_full_database

from .object import *
from .CONTENTS import (
    TEXT_COLOR_LIST, 
    ROLLUP_FUNCTION_LIST, 
    BLOCK_TYPE_LIST,
    CODE_LANGUAGE_LIST,
    MEDIA_TYPE_LIST,
    NON_CREATEABLE_PROPERTIES_TYPES,
    )

class Property_gadget:
    @staticmethod
    def is_exist(prop_dict:dict, target:list) ->bool:
        """
        Check if the prop_dict is exist in dict of list
        
        Parameters:
            prop_dict:          (dict)      - Target dict to check
            target:             (list)      - Target list to check

        Returns:
            result:             (bool)      - Result
        """
        for target_dict in target:
            # Check 'name' and 'id' key
            if (('name' in prop_dict) and (prop_dict['name'] == target_dict['name'])) or \
                (('id' in prop_dict) and (prop_dict['id'] == target_dict['id'])):
                 return True
        return False

    @staticmethod
    def get_properties_name(database_properties_dict:dict, type:str) ->list:
        """
        Get properties name

        Parameters:
            database_properties_dict:    (dict)      - Target properties dict of database
            type:                        (str)       - Target properties type

        Returns:
            (list)  - Target property names
        """
        keys = []
        for key, item in database_properties_dict.items():
            if item['type'] == type:
                keys.append(key)
        return keys
    
    @staticmethod
    def get_property_dict(database_properties_dict:dict, name:str) ->dict:
        """
        Get property dict

        Parameters:
            database_properties_dict:    (dict)      - Target properties dict of database
            name:                        (str)       - Target properties name

        Returns:
            (dict)  - Target property dict
        """
        return {name: database_properties_dict[name]}
    
    @staticmethod
    def del_properties(database_properties_dict:dict, names:list) -> None:
        """
        Delete properties

        Parameters:
            database_properties_dict:    (dict)      - Target properties dict of database
            name:                        (str)       - Target properties name

        Returns:
            (dict)  - Target properties dict
        """
        if not (names == []):
            for name in names:
                database_properties_dict.pop(name)
    
    # FC: [Get property type dict]
    @staticmethod
    def create_dict(name:str, type:str, **kwargs) ->dict:
        """
        Create properties

        Parameters:
            name:           (str)       - Properties name
            type:           (str)       - Properties type
            **kwargs:       (dict)      - Properties options
                exsampe:
                    format:     (str)       - Number format
                    options:    (list)      - Select and Multi-select options
                    expression: (str)       - Formula expression
                       
        Return:
            properties:     (dict)      - Properties dict
            
        Raises:
            Exception:      (Exception) - Error type value
        """
        if type == 'rich_text':
            # return {name: {'rich_text': {},
            #                'name': name,
            #                'type': 'rich_text'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'number':
            # if kwargs == {}:
            #     kwargs = {'format': 'number'}
            # return {name: {'number': kwargs,
            #                'name': name,
            #                'type': 'number'}}
            return PropertyType(name=name, type=type,
                                number=Number() if kwargs == {} else Number(**kwargs)
                                ).full_dict()            
        elif type == 'select':
            # if kwargs == {}:
            #     kwargs = {'options': []}
            # return {name: {'select': kwargs,
            #                'name': name,
            #                'type': 'select'}}
            return PropertyType(name=name, type=type,
                                select=Options() if kwargs == {} else Options(**kwargs)
                                ).full_dict()
        elif type == 'multi_select':
            # if kwargs == {}:
            #     kwargs = {'options': []}
            # return {name: {'multi_select': kwargs,
            #                 'name': name,
            #                 'type': 'multi_select'}}
            return PropertyType(name=name, type=type,
                                multi_select=Options() if kwargs == {} else Options(**kwargs)
                                ).full_dict()
        elif type == 'date':
            # return {name: {'date': {},
            #                'name': name,
            #                'type': 'date'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'people':
            # return {name: {'people': {},
            #                'name': name,
            #                'type': 'people'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'files':
            # return {name: {'files': {},
            #                 'name': name,
            #                 'type': 'files'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'checkbox':
            # return {name: {'checkbox': {},
            #                'name': name,
            #                'type': 'checkbox'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'url':
            # return {name: {'url': {},
            #                'name': name,
            #                'type': 'url'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'email':
            # return {name: {'email': {},
            #                'name': name,
            #                'type': 'email'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'phone_number':
            # return {name: {'phone_number': {},
            #                'name': name,
            #                'type': 'phone_number'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'formula':
            # if kwargs == {}:
            #     kwargs = {'expression': ''}
            # return {name: {'formula': kwargs,
            #                'name': name,
            #                'type': 'formula'}}
            return PropertyType(name=name, type=type,
                                formula=Formula() if kwargs == {} else Formula(**kwargs)).full_dict()
        elif type == 'relation':
            if kwargs == {} or not ('relation' in kwargs):
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                 "Parameter error, please check. " +
                                 "Relation properties need to set 'relation' key." +
                                 "Recommend to use 'gadget.create_relation_dict' method.")
            # return {name: {'relation': kwargs['relation_dict'],
            #                'name': name,
            #                'type': 'relation'}}
            return PropertyType(name=name, type=type,
                                relation=kwargs['relation']).full_dict()
        elif type == 'rollup':
            if kwargs == {} or not ('rollup_dict' in kwargs):
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                 "Parameter error, please check. " +
                                 "Rollup properties need to set 'rollup_dict' key." +
                                 "Recommend to use 'gadget.create_rollup_dict' method.")
            # return {name: {'rollup': kwargs['rollup_dict'],
            #                'name': name,
            #                'type': 'rollup'}}
            return PropertyType(name=name, type=type,
                                rollup=kwargs['rollup']).full_dict()
        elif type == 'created_time':
            # return {name: {'created_time': {},
            #                'name': name,
            #                'type': 'created_time'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'created_by':
            # return {name: {'created_by': {},
            #                'name': name,
            #                'type': 'created_by'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'last_edited_time':
            # return {name: {'last_edited_time': {},
            #                'name': name,
            #                'type': 'last_edited_time'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'last_edited_by':
            # return {name: {'last_edited_by': {},
            #                'name': name,
            #                'type': 'last_edited_by'}}
            return PropertyType(name=name, type=type).full_dict()
        elif type == 'status':
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'status' is not support.")
        else:
            raise Exception(f"{sys._getframe().f_code.co_name}: " + 
                            "Parameter error, please check the parameter. " +
                            "'type' is not in 'rich_text', 'number', 'select', 'multi_select', 'date', 'people', 'file', 'checkbox', 'url', 'email', 'phone_number', 'formula', 'relation', 'rollup', 'created_time', 'created_by', 'last_edited_time', 'last_edited_by'")
    
    ## Property
    ### Set property name
    @staticmethod
    def set_property_name(property_dict:dict, name:str) ->dict:
        """
        Set property name

        Parameters:
            property_dict:        (dict)      - property dict
            name:                 (str)       - New name
            
        Return:
            new_property_dict:    (dict)      - New property dict
        """
        for _,items in property_dict.items():
            items['name'] = name
        return property_dict
    
    ### Rename property name
    @staticmethod
    def rename_property(old_name:str, new_name:str) ->dict:
        """
        Rename property name

        Parameters:
            old_name:        (str)       - Old name
            new_name:        (str)       - New name
            
        Return:
            property_dict:   (dict)      - New property dict
        """
        return {old_name:{'name':new_name}}
        
    ### Mix properties
    @staticmethod
    def mix_properties(*args) ->dict:
        """
        Mix properties

        Parameters:
            *args:        (dict)      - properties dict
            
        Return:
            properties:   (dict)      - New properties dict
        """
        properties = {}
        for arg in args:
            properties.update(arg)
        return properties
      
    ### Text
    #### Page
    @staticmethod
    def set_text(name:str, text:str, **kwargs) ->dict:
        """
        Create new text properties dict

        Args:
            name:     (str)              - Name of text properties
            text:     (list or dict)     - properties
            **kwargs: (dict)             - Text style

        Returns:
            text:     (dict)             - new text properties dict
        """
        new_text =  {'text': {'content': text}}
        if 'style' in kwargs:
            new_text.update({'annotations':kwargs['style']})
        else:
            new_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        return {name: {'rich_text': [new_text]}}

    @staticmethod
    def set_text_style(bold:bool=False, code:bool=False,
                       color:str='default', italic:bool=False,
                       strikethrough:bool=False, underline:bool=False,)->dict:
        return {'bold': bold, 'code': code, 'color': color, 'italic': italic, 'strikethrough': strikethrough, 'underline': underline}
    
    @staticmethod
    def update_text_style(text:dict, style:dict) ->dict:
        """
        Mix text style

        Parameters:
            text:          (dict)      - Text dict
            style:         (dict)      - Style dict
            
        Return:
            text:          (dict)      - Text dict
        """
        for _, item in text.items():
            item['rich_text'][0]['annotations'] = style
        return text
    
    @staticmethod
    def add_next_line(text:dict) ->dict:
        """
        Set next line
        
        Parameters:
            text:          (dict)      - Text dict
            
        Return:
            text:          (dict)      - Text dict
        """
        next_line = {'annotations': {'bold': False,
                                'code': False,
                                'color': 'default',
                                'italic': False,
                                'strikethrough': False,
                                'underline': False},
                'href': None,
                'plain_text': '\n',
                'text': {'content': '\n', 'link': None},
                'type': 'text'}
        for _, item in text.items():
            item['rich_text'].append(next_line)
        return text
    
    @staticmethod
    def add_new_text(text_dict:dict, new_text:str, **kwargs) ->dict:
        """
        Add new text

        Parameters:
            text_dict:     (dict)      - Text dict
            new_text:      (str)       - New text
            **kwargs:      (dict)      - Text style
            
        Return:
            text_dict:     (dict)      - Text dict
        """
        new_text_dict =  {'text': {'content': new_text}}
        new_text_dict.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        for _, item in text_dict.items():
            item['rich_text'].append(new_text_dict)
        return text_dict
    
    @staticmethod
    def add_metion(text_dict:dict, dict:dict, **kwargs) ->dict:
        """
        Add metion

        Parameters:
            text_dict:     (dict)      - Text dict
            dict:          (dict)      - Metion dict is maybe page or database
            **kwargs:      (dict)      - Text style
            
        Return:
            text_dict:     (dict)      - Text dict
            
        Raises:
            Exception:     (Exception) - dict is not page or database
        """
        type = Dict_Gadget.check_dict_type(dict)
        if type == 'none':
            raise Exception('dict is not page or database')
        
        metion_dict= {'href': 'https://www.notion.so/'+dict['id'],
                      'type': 'mention'}
        if type == 'page':
            metion_dict.update({'mention': {'page': {'id': dict['id']},
                                            'type': 'page'},
                                'plain_text': Page_gadget.get_title(dict)})
        elif type == 'database':
            metion_dict.update({'mention': {'database': {'id': dict['id']},
                                            'type': 'database'},
                                'plain_text': Database_gadget.get_title(dict)})
        
        metion_dict.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        for _, item in text_dict.items():
            item['rich_text'].append(metion_dict)
        return text_dict
    
    @staticmethod
    def add_hyperlink(text_dict:dict, text:str, link:str, **kwargs) ->dict:
        """
        Add hyperlink

        Parameters:
            text_dict:     (dict)      - Text dict
            text:          (str)       - Text
            link:          (str)       - Hyperlink url
            **kwargs:      (dict)      - Text style
            
        Return:
            text_dict:     (dict)      - Text dict
            
        Raises:
            Exception:     (Exception) - dict is not page or database
        """
        hyperlink_dict = {
                          'text':{'content': text,
                                  'link': {'url': link}},
                          'type': 'text'}
        hyperlink_dict.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        for _, item in text_dict.items():
            item['rich_text'].append(hyperlink_dict)
        return text_dict
        
    @staticmethod
    def mix_text(*args) ->dict:
        """
        Mix text

        Parameters:
            *args:        (dict)      - Text dict   
            
        Return:
            text:          (dict)      - Text dict
        """
        text = args[0]
        new_text = args[1]
        
        new_text_dict = {}
        for _, item in new_text.items():
            new_text_dict = item['rich_text'][0]
        for _, item in text.items():
            item['rich_text'].append(new_text_dict)
        return text
    
    ### Checkbox
    @staticmethod
    def set_checkbox(name:str, checked:bool) ->dict:
        """
        Set checkbox

        Parameters:
            name:               (str)       - Name of checkbox property
            checked:            (bool)      - Checkbox checked
            
        Return:
            checkbox_dict:      (dict)      - Checkbox dict
        """
        return {name: {'checkbox': checked}}
    
    ### Number
    #### Database
    @staticmethod
    def set_number_format(number_dict:dict, format:str) ->dict:
        """
        Set number format

        Parameters:
            number_dict:        (dict)      - Number dict
            format:             (str)       - Number format
            
        Return:
            new_number_dict:    (dict)      - New number dict
        """
        for _, item in number_dict.items():
            item['number']['format'] = format
        return number_dict
    
    #### Page
    @staticmethod
    def set_number(name:str, number:float) ->dict:
        """
        Set number

        Parameters:
            name:               (str)       - Name of number property
            number:             (float)     - Number
            
        Return:
            number_dict:        (dict)      - Number dict
        """
        return {name: {'number': number}}
    
    ### Select
    #### Function
    @staticmethod
    def check_select_option(options_list:list, option:str) ->bool:
        """
        Check select option if in options list

        Args:
            options_list    (list):     - Select options list
            option          (str):      - Select option

        Returns:
            bool:                       - True if in options list, else False
        """
        if option in options_list:
            return True
        else:
            return False
    
    @staticmethod
    def set_select_option(option_name:list, option_color:list) ->list:
        """
        Set select option

        Parameters:
            option_name:            (list)      - Option name list
            option_color:           (list)      - Option color list
            
        Return:
            option_list:            (list)      - Option list
        """
        option_list = []
        for i in range(len(option_name)):
            option_list.append({'name': option_name[i],
                                'color': option_color[i]})
        return option_list
    
    #### Database
    @staticmethod
    def get_select_options_list(database_property_dict:dict, select_name:str) ->list:
        """
        Set select options list

        Parameters:
            database_property_dict:        (dict)      - property dict
            select_name:                   (str)       - select name
            
        Return:
            options_list:                  (list)      - select options list
        """
        options_list = []
        for option in database_property_dict[select_name]['select']['options']:
            options_list.append(option['name'])
        return options_list
    
    #### Page
    @staticmethod
    def set_select(name:str, option:str) ->dict:
        """
        Set select

        Parameters:
            name:               (str)       - Name of select property
            option:             (str)       - Select dict
            
        Return:
            select_dict:        (dict)      - Select dict
        """
        return {name: {'select':  {'name': option}}}
    
    ### Multi-Select
    #### Database
    @staticmethod
    def get_multi_select_options_list(database_property_dict:dict, select_name:str) ->list:
        """
        Set multi_select options list

        Parameters:
            database_property_dict:        (dict)      - property dict
            select_name:                   (str)       - select name
            
        Return:
            options_list:                  (list)      - select options list
        """
        options_list = []
        for option in database_property_dict[select_name]['multi_select']['options']:
            options_list.append(option['name'])
        return options_list
    
    #### Page
    @staticmethod
    def set_multi_select(name:str, options:list) ->dict:
        """
        Set multi_select

        Parameters:
            name:               (str)       - Name of select property
            options:            (list)      - Select dict
            
        Return:
            multi_select_dict:  (dict)      - Select dict
        """
        multi_select_dict =  {name: {'multi_select': []}}
        for option in options:
            multi_select_dict[name]['multi_select'].append({'name': option})
        return multi_select_dict
    
    ### Date
    @staticmethod
    def set_date(name:str, start_date:str, end_date:Any=None) ->dict:
        """
        Set date

        Parameters:
            name:               (str)       - Name of date property ex: 'YYYY-MM-DDThh:mm:ss.000+09:00'
            start_date:         (str)       - Start date ex: 'YYYY-MM-DDThh:mm:ss.000+09:00'
            end_date:           (str)       - End date
            
        Return:
            date_dict:          (dict)      - Date dict
        """
        return {name: {'date': {'start': start_date, 'end': end_date, 'time_zone': None}}}
    
    ### Status
    @staticmethod
    def get_status_options_dict(database_property_dict:dict, status_name:str) ->dict:
        """
        Get status options dict

        Parameters:
            database_property_dict:        (dict)      - property dict
            status_name:                   (str)       - status name
            
        Return:
            options_dict:                  (dict)      - status options dict
                Ex:
                    {'group name1': [{'color': 'gray', 'name': 'Not Started'},
                                {'color': 'yellow', 'name': 'Todo'}],
                    'group name2': [{'color': 'green', 'name': 'Done'}]}
            
        """
        options_dict = {}
        # Get group name
        for group in database_property_dict[status_name]['status']['groups']:
            options_dict.update({group['name']: group['option_ids']})
        
        # Get options
        for option in database_property_dict[status_name]['status']['options']:
            for _,ids in options_dict.items():
                if option['id'] in ids:
                    ids.remove(option['id'])
                    ids.append(option['name'])
            
        return options_dict
    
    @staticmethod
    def set_status(name:str, option:str) ->dict:
        """
        Set status

        Parameters:
            name:               (str)       - Name of status property
            option:             (str)       - Status option
            
        Return:
            status_dict:        (dict)      - Status dict
        """
        return {name: {'status': {'name': option}}}
    
    ### Email
    @staticmethod
    def set_email(name:str, email:str) ->dict:
        """
        Set email

        Parameters:
            name:               (str)       - Name of email property
            email:              (str)       - Email
            
        Return:
            email_dict:         (dict)      - Email dict
        """
        return {name: {'email': email}}
    
    ### Files
    @staticmethod
    def get_files_path(page_property_dict:dict, files_name:str) ->list:
        """
        Get files path

        Parameters:
            page_property_dict:        (dict)      - property dict
            files_name:                (str)       - files property name
            
        Return:
            files_path:                (list)      - files path
        """
        files_path = []
        for file in page_property_dict[files_name]['files']:
            files_path.append(file)
        return files_path
    
    @staticmethod
    def del_files(name:str) ->dict:
        """
        Delete files

        Parameters:
            name:               (str)       - Name of files property
            
        Return:
            files_dict:         (dict)      - Files dict
        """
        return {name: {'files': []}}
    
    @staticmethod
    def pass_files(name:str, files_path:list) ->dict:
        """
        Pass files

        Parameters:
            name:               (str)       - Name of files property
            files_path:         (list)      - Files path
            
        Return:
            files_dict:         (dict)      - Files dict
        """
        # check path
        for path in files_path:
            # check file
            if 'type' in path \
                and ((path['type'] == 'file' and 'file' in path \
                        and 'expiry_time' in path['file'] \
                        and 'url' in path['file']) \
                    or (path['type'] == 'external' and 'external'in path \
                        and 'url' in path['external'])):
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'files_path' is not form notion api. " +
                                "(https://developers.notion.com/reference/file-object)")
                
        return {name: {'files': files_path}}
    
    ### Phone Number
    @staticmethod
    def set_phone_number(name:str, phone_number:str) ->dict:
        """
        Set phone number

        Parameters:
            name:               (str)       - Name of phone number property
            phone_number:       (str)       - Phone number
            
        Return:
            phone_number_dict:  (dict)      - Phone number dict
        """
        return {name: {'phone_number': phone_number}}
    
    ### People
    @staticmethod
    def set_people(name:str, people_dicts:list) ->dict:
        """
        Set people

        Parameters:
            name:               (str)       - Name of people property
            people_dicts:       (list)      - People dict of list
            
        Return:
            people_dict:        (dict)      - People dict
        """
        return {name: {'people': people_dicts}}
    
    @staticmethod
    def del_pepole(name:str) ->dict:
        """
        Delete people

        Parameters:
            name:               (str)       - Name of people property
            
        Return:
            people_dict:        (dict)      - People dict
        """
        return {name: {'people': []}}
    
    ### Url
    @staticmethod
    def set_url(name:str, url:str) ->dict:
        """
        Set url

        Parameters:
            name:               (str)       - Name of url property
            url:                (str)       - Url
            
        Return:
            url_dict:           (dict)      - Url dict
        """
        return {name: {'url': url}}
    
    ### Rollup
    @staticmethod
    def create_rollup_dict(function:str, relation_property_name:str, rollup_property_name:str) ->dict:
        """
        Get rollup dict

        Parameters:
            function:                   (str)       - Rollup function
            relation_property_name:     (str)       - Relation property name
            rollup_property_name:       (str)       - Rollup property name
            
        Return:
            rollup_dict:                (dict)      - Rollup dict
            
        Raise:
            Exception:                  (Exception) - Parameter error
        """
        if not Dict_Gadget.check_rollup_function(function):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                             "Parameter error, please check the parameter. " +
                            f"'function' is not in ROLLUP_FUNCTION_LIST. \n" +
                            f" ROLLUP_FUNCTION_LIST: {ROLLUP_FUNCTION_LIST}")
        return {'function': function,
                'relation_property_name': relation_property_name,
                'rollup_property_name': rollup_property_name}
        
    @staticmethod
    def get_rollup_value(page_property_dict:dict, rollup_property_name:str) ->dict:
        """
        Get rollup value

        Parameters:
            page_property_dict:         (dict)      - Property dict
            rollup_property_name:       (str)       - Rollup property name
            
        Return:
            rollup_value:               (dict)      - Rollup value
        """
        return page_property_dict[rollup_property_name]['rollup']
    
    ### Relation
    @staticmethod
    def create_relation_dict(database_id:str, is_dual:bool) ->dict:
        """
        Get relation dict

        Parameters:
            database_id:        (str)       - Database id
            is_dual:            (bool)      - If is 'dual_property' will be true
            
        Return:
            relation_dict:      (dict)      - Relation dict
        """
        if is_dual:
            # relation_dict = {'database_id': database_id,
            #                   'type': 'dual_property',
            #                   'dual_property': {},
            #                 }
            relation_dict = RelationDual(database_id=database_id).asdict()
        else:
            # relation_dict = {'database_id': database_id,
            #                  'type': 'single_property',
            #                  'single_property': {},
            #                 }
            relation_dict = RelationSingle(database_id=database_id).asdict()
        return relation_dict
    
    @staticmethod
    def set_relation(name:str, relation_ids:list) ->dict:
        """
        Set relation

        Parameters:
            name:               (str)       - Name of relation property
            relation_id:        (list)       - Relation ids
            
        Return:
            relation_dict:      (dict)      - Relation dict
        """
        ids = []
        for id in relation_ids:
            ids.append({'id': id})
        return {name: {'relation': ids}}
    
class Page_gadget:
    @staticmethod
    def get_id(page_dict:dict) ->str:
        """
        Get page id from raw dict

        Patameters:
            page_dict:          (dict)      - Raw page dict form Client.pages.retrieve()
        
        Return
            page_id:            (str)       - Page id
        """
        if 'object' in page_dict and page_dict['object'] == 'page':
            return page_dict['id']
        else:
            raise Exception(f"{sys._getframe().f_code.co_name}: " + 
                            "Parameter error, please check the parameter. " +
                            "'page_dict' is not form Client.pages.retrieve()")
    
    @staticmethod
    def get_title(page_dict:dict) ->Any:
        """
        Get page title
        
        Parameters:
            page_dict:          (dict)      - Raw page dict form Client.pages.retrieve()   ** Choose one of the two parameters **
        
        Returns:
            title:              (str)       - Target page title
        """
        if 'object' in page_dict and page_dict['object'] == 'page':
            properties_data = page_dict['properties']
        else: 
            raise Exception(f"{sys._getframe().f_code.co_name}:  " +
                            "Parameter error, please check the parameter. " +
                            "'page_dict' is not form Client.pages.retrieve()")

        for item in properties_data.items():
            if item[1]['type'] == 'title':
                return item[1]['title'][0]['plain_text']
            
    @staticmethod
    def get_info(page_dict:dict={}) ->dict:
        """
        Get page information

        Parameters:
            page_dict:          (dict)      - Raw page dict form Client.pages.retrieve()
            
        Returns:
            page_info:          (dict)      - Target page information
                                            - exsample:[{'name': "",
                                                         'id': "",
                                                         'properties: [{'name': "",
                                                                        'value': {}}, {...}],
                                                        }, {...}]
        """
        if not ('object' in page_dict and page_dict['object'] == 'page'): 
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'page_dict' is not form Client.pages.retrieve()")
            
        page_info = {'name': Page_gadget.get_title(page_dict=page_dict),
                    'id': page_dict['id'],
                    'properties': page_dict['properties']}
        return page_info
    
    @staticmethod
    def get_properties(page_dict:dict) ->dict:
        """
        Get page properites from page info dict

        Parameters:
            page_dict:          (dict)      - Raw page dict form Client.pages.retrieve()
        
        Return:
            page_properties:    (dict)      - Target page properties
        """
        if 'properties' in page_dict:
            return page_dict['properties']
        else:
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "page dict not include 'property'")
    
class Database_gadget:
    @staticmethod
    def get_id(database_dict:dict) ->str:
        """
        Get database title
        
        Parameters:
            database_dict:      (dict)      - Raw page dict form Client.pages.retrieve()   ** Choose one of the two parameters **
        
        Returns:
            title:              (str)       - Target page title
        """
        if 'object' in database_dict and database_dict['object'] == 'database':
            return database_dict['id']
        else: 
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'database_dict' is not form Client.databases.retrieve()")
    
    @staticmethod
    def get_title(database_dict:dict) ->str:
        """
        Get database title
        
        Parameters:
            database_dict:      (dict)      - Raw page dict form Client.pages.retrieve()   ** Choose one of the two parameters **
        
        Returns:
            title:              (str)       - Target page title
        """
        if 'object' in database_dict and database_dict['object'] == 'database':
            return database_dict['title'][0]['plain_text']
        else: 
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'database_dict' is not form Client.databases.retrieve()")

    @staticmethod
    def get_pages_list(database_page_dict:dict={}) ->list:
        """
        Get page list in the database of table

        Parameters:
            database:           (dict)      - Target database dict form Client.databases.query()
            
        Returns:
            page_list:          (list)      - Target page list
                                            - exsample:[{'name': "",
                                                         'id': ""}, {...}]                                        
        """
        if 'object' in  database_page_dict \
                    and database_page_dict['object'] == 'list' :
            pages_list = database_page_dict['results']
        else:
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'database_page_dict' is not form Client.databases.query()")
        page_list = []
        for page in pages_list:
            page_list.append({'name': Page_gadget.get_title(page),
                              'id':page['id']})
        return page_list
    
    @staticmethod
    def get_properties_options_dict(database_dict:dict={}) ->dict:
        """
        Get properties list in the database of table

        Parameters:
            database_dict:      (dict)      - Target database dict form Client.databases.retrieve()
        Returns:
            properties_dict:    (dict)      - Target properties dict
                                            - exsample:{'name': {'id': "",
                                                                'type': "",
                                                                'value': {}
                                                                }, 
                                                        ...
                                                        }
        """
        if 'object' in  database_dict \
                    and database_dict['object'] == 'database':
            properties = database_dict['properties']
        else:
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter." +
                            "'database_dict' is not form Client.databases.retrieve()")

        properties_dict = {}
        for key, item in properties.items():
            properties_dict.update({key: {'id': item['id'],
                                          'type': item['type'],
                                           item['type']: item[item['type']]}})
            
        return properties_dict
                    
class Block_gadget:
    @staticmethod
    def get_block_ids_and_type(block_dict:dict) ->list:
        """
        Get block ids
        
        Parameters:
            block_dict:         (dict)      - Target block dict
            
        Returns:
            block_infos:          (list)      - Target block ids
                                            - exsample:[{'type': 'page',
                                                        'ids': ['id1']},
                                                        ...]
            
        Raises:
            Exception:          (Exception) - block dict not include 'results
        """
        if 'results' not in block_dict:
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "block dict not include 'results'")
        blocks_info = []
        for block in block_dict['results']:
            blocks_info.append({'type': block['type'],
                            'id': block['id']})
        return blocks_info
    
    @staticmethod
    def get_block_id(blocks_info:list, type:str) ->str:
        """
        Take block id
        
        Parameters:
            blocks_info:        (list)      - Target block info list
            
        Returns:
            block_id:           (str)       - Target block id
        """
        if type == 'text':
            type = 'paragraph'
        for block_info in blocks_info:
            if block_info['type'] == type:
                return block_info['id']
        return ""
    
    @staticmethod
    def get_generic_block_dict(type:str ,**kwargs) ->dict:
        """
        Get block dict
        
        Parameters:
            type:               (str)       - Target block type
            kwargs:             (dict)      - Target block data
            
        Returns:
            block_dict:         (dict)      - Target block dict
        """
        if not Dict_Gadget.check_block_type(type):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'type' is not in BLOCK_TYPE_LIST. \n" +
                            f"BLOCK_TYPE_LIST = {BLOCK_TYPE_LIST}")
        block_dict = {'object': 'block',
                      'type': type,
                    }
        
        if (type == 'heading_1' or
            type == 'heading_2' or
            type == 'heading_3'):
            block_dict.update(kwargs['text'])
            kwargs.pop('text')
            if 'is_toggleable' in kwargs:
                block_dict[type].update({'is_toggleable': kwargs['is_toggleable']})  # type: ignore "block_dict[type] is dict"
                kwargs.pop('is_toggleable')
        
        block_dict.update(kwargs)
        return block_dict
 
    # FC: [Block dict] paragraph
    @staticmethod
    def get_text_block(text:str, **kwargs) ->dict:
        """
        Get paragraph block dict
        
        Parameters:
            text:               (str)       - Target block text
            kwargs:             (dict)      - Target block data
            
        Returns:
            paragraph_block:    (dict)      - Target block dict
        """
        type = 'paragraph'
        paragraph_text = {'text': {'content': text}}
        if 'style' in kwargs:
            paragraph_text.update({'annotations':kwargs['style']})
        else:
            paragraph_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        paragraph_block = {'type': type,
                           type:{'rich_text': [paragraph_text]},
                        }
        
        return paragraph_block    
    
    # FC: [Block dict] heading
    @staticmethod
    def get_heading_block(text:str, type:str, is_toggleable:bool=False, **kwargs) ->dict:
        """
        Get heading block dict
        
        Parameters:
            text:               (str)       - Target block text
            type:               (str)       - Target block type
            is_toggleable:      (bool)      - Target block is toggleable
            kwargs:             (dict)      - Target block data
            
        Returns:
            heading_block:         (dict)      - Target block dict
            
        Raises:
            Exception:          (Exception) - Parameter error
        """        
        if not (type == 'heading_1' or
                type == 'heading_2' or
                type == 'heading_3'):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'type' is not in ['heading_1', 'heading_2', 'heading_3'].")
        
        title_text = {'text': {'content': text}}
        if 'style' in kwargs:
            title_text.update({'annotations':kwargs['style']})
        else:
            title_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        heading_block = {'type': type,
                        type:{'rich_text': [title_text],
                              'is_toggleable': is_toggleable,
                              },
                        }
        return heading_block
    
    # FC: [Block dict] callout
    @staticmethod
    def get_callout_block(text:str, icon:str="📦", **kwargs) ->dict:
        """
        Get callout block dict
        
        Parameters:
            text:               (str)       - Target block text
            icon:               (str)       - Target block icon
            kwargs:             (dict)      - Target block data
            
        Returns:
            callout_block:         (dict)      - Target block dict
        """
        type = 'callout'
        callout_text = {'text': {'content': text}}
        if 'style' in kwargs:
            callout_text.update({'annotations':kwargs['style']})
        else:
            callout_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        callout_block = {'type': type,
                         type: {
                                'rich_text': [callout_text]
                                },
                        }
        
        return callout_block  
        
    # FC: [Block dict] quote list
    @staticmethod
    def get_quote_block(text:str, color:str="default", **kwargs) ->dict:
        """
        Get quote block dict
        
        Parameters:
            text:               (str)        - Target block text
            kwargs:             (dict)       - Target block data
            
        Returns:
            quote_block:        (dict)       - Target block dict
            
        Raises:
            Exception:          (Exception)  - Parameter error
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in TEXT_COLOR_LIST. \n" +
                            f"TEXT_COLOR_LIST = {TEXT_COLOR_LIST}")
            
        type = 'quote'
        quote_text = {'text': {'content': text}}
        if 'style' in kwargs:
            quote_text.update({'annotations':kwargs['style']})
        else:
            quote_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        quote_block = {'type': type,
                       type: {
                             'rich_text': [quote_text],
                             'color': color,
                             },
                      }
        if "children" in kwargs:
            if type(kwargs["children"]) is list: # type: ignore "kwargs["children"] need be is list"
                quote_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")

        return quote_block
    
    # FC: [Block dict] bulleted list
    @staticmethod
    def get_bulleted_list_block(text:str, color:str="default", **kwargs) ->dict:
        """
        Get bulleted list block dict
        
        Parameters:
            items:                    (list)      - Target block items
            kwargs:                   (dict)      - Target block data
            
        Returns:
            bulleted_list_block:      (dict)      - Target block dict
            
        Raises:
            Exception:                (Exception) - Parameter error
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in TEXT_COLOR_LIST. \n" +
                            f"TEXT_COLOR_LIST = {TEXT_COLOR_LIST}")
        
        type = 'bulleted_list_item'
        bulleted_list_text = {'text': {'content': text}}
        if 'style' in kwargs:
            bulleted_list_text.update({'annotations':kwargs['style']})
        else:
            bulleted_list_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        bulleted_list_block = {'type': type,
                                type: {
                                        'rich_text': [bulleted_list_text],
                                        'color': color,
                                      },
                                }

        if "children" in kwargs:
            if type(kwargs["children"]) is list: # type: ignore "kwargs["children"] need be is list"
                bulleted_list_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")

        return bulleted_list_block  
    
    # FC: [Block dict] numbered list
    @staticmethod
    def get_numbered_list_block(text:str, color:str="default", **kwargs) ->dict:
        """
        Get numbered list block dict
        
        Parameters:
            items:                   (list)      - Target block items
            kwargs:                  (dict)      - Target block data
            
        Returns:
            numbered_list_block:     (dict)      - Target block dict
            
        Raises:
            Exception:               (Exception) - Parameter error
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in TEXT_COLOR_LIST. \n" +
                            f"TEXT_COLOR_LIST = {TEXT_COLOR_LIST}")
        
        type = 'numbered_list_item'
        numbered_list_text = {'text': {'content': text}}
        if 'style' in kwargs:
            numbered_list_text.update({'annotations':kwargs['style']})
        else:
            numbered_list_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        numbered_list_block = {'type': type,
                                type: {
                                        'rich_text': [numbered_list_text],
                                        'color': color,
                                      },
                                }

        if "children" in kwargs:
            if type(kwargs["children"]) is list:  # type: ignore "kwargs["children"] need be is list"
                numbered_list_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")
                
        return numbered_list_block
    
    # FC: [Block dict] to do list
    @staticmethod
    def get_to_do_list_block(text:str, checked:bool=False, color:str="default", **kwargs) ->dict:
        """
        Get to do list block dict
        
        Parameters:
            text:                   (str)       - Target block text
            checked:                (bool)      - Target block checked
            kwargs:                 (dict)      - Target block data
            
        Returns:
            to_do_list_block:       (dict)      - Target block dict
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in TEXT_COLOR_LIST. \n" +
                            f"TEXT_COLOR_LIST = {TEXT_COLOR_LIST}")
        
        type = 'to_do'
        to_do_list_text = {'text': {'content': text}}
        if 'style' in kwargs:
            to_do_list_text.update({'annotations':kwargs['style']})
        else:
            to_do_list_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        to_do_list_block = {'type': type,
                            type: {
                                    'rich_text': [to_do_list_text],
                                    'checked': checked,
                                    'color': color,
                                  },
                            }
        
        if "children" in kwargs:
            if type(kwargs["children"]) is list:  # type: ignore "kwargs["children"] need be is list"
                to_do_list_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")
                
        return to_do_list_block
    
    # FC: [Block dict] toggle list
    @staticmethod
    def get_toggle_list_block(text:str, color:str="default", **kwargs) ->dict:
        """
        Get toggle list block dict
        
        Parameters:
            text:                   (str)       - Target block text
            kwargs:                 (dict)      - Target block data
            
        Returns:
            toggle_list_block:      (dict)      - Target block dict
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in TEXT_COLOR_LIST. \n" +
                            f"TEXT_COLOR_LIST = {TEXT_COLOR_LIST}")
        
        type = 'toggle'
        toggle_list_text = {'text': {'content': text}}
        if 'style' in kwargs:
            toggle_list_text.update({'annotations':kwargs['style']})
        else:
            toggle_list_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
        
        toggle_list_block = {'type': type,
                            type: {
                                    'rich_text': [toggle_list_text],
                                    'color': color,
                                  },
                            }
        
        if "children" in kwargs:
            if type(kwargs["children"]) is list:   # type: ignore "kwargs["children"] need be is list"
                toggle_list_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")
                
        return toggle_list_block
    
    # FC: [Block dict] code page
    @staticmethod
    def get_code_page_block(text:str, language:str="plaintext") ->dict:
        """
        Get code page block dict
        
        Parameters:
            text:                   (str)       - Target block text
            language:               (str)       - Target block language
            
        Returns:
            code_page_block:        (dict)      - Target block dict
        """
        if not Dict_Gadget.check_code_language(language):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'language' is not in CODE_LANGUAGE_LIST. \n" +
                            f"CODE_LANGUAGE_LIST = {CODE_LANGUAGE_LIST}")
            
        type = 'code'
        code_page_block = {'type': type,
                            type: {
                                    'type': "text",
                                    'text': {'content': text
                                            },
                                    'language': language,
                                  },
                            }
        
        return code_page_block
        
    # FC: [Block dict] child page
    # TODO: untest
    # WARNING: To create or update child_page type blocks, use the "Create Page" and the "Update page" endpoint.
    @staticmethod
    def get_child_page_block(title:str) ->dict:
        """
        Get child page block dict
        
        Parameters:
            child_page_id:          (str)       - Target block child page id
            title:                  (str)       - Target block title
            kwargs:                 (dict)      - Target block data
            
        Returns:
            child_page_block:       (dict)      - Target block dict
        """
        type = 'child_page'
        child_page_block = {'type': type,
                            type: {
                                    'title': title,
                                  },
                            }
        return child_page_block
    
    # FC: [Block dict] child database
    # WARNING: To create or update child_database type blocks, use the "Create database" and the "Update database" endpoint.
    @staticmethod
    def get_child_database_block(title:str) ->dict:
        """
        Get child database block dict
        
        Parameters:
            child_database_id:     (str)       - Target block child database id
            title:                  (str)       - Target block title
            kwargs:                 (dict)      - Target block data
            
        Returns:
            child_database_block:  (dict)      - Target block dict
        """
        type = 'child_database'
        child_database_block = {'type': type,
                                type: {
                                        'title': title,
                                    },
                                }
        return child_database_block
    
    # FC: [Block dict] embed block
    @staticmethod
    def get_embed_block(url:str) ->dict:
        """
        Get embed block dict
        
        Parameters:
            url:                    (str)       - Target block url
            
        Returns:
            embed_block:            (dict)      - Target block dict
        """
        type = 'embed'
        embed_block = {'type': type,
                        type: {
                                'url': url,
                                },
                        }
        return embed_block
    
    # FC: [Block dict] media block
    @staticmethod
    def get_media_block(url:str, type:str) ->dict:
        """
        Get image block dict
        
        Parameters:
            image_url:              (str)       - Target block image url
            
        Returns:
            image_block:            (dict)      - Target block dict
            
        Raises:
            Exception:              (Exception) - Parameter error
        """
        if not Dict_Gadget.check_media_type(type):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'type' is not in MEDIA_TYPE_LIST. \n" +
                            f"MEDIA_TYPE_LIST = {MEDIA_TYPE_LIST}")
        media_block = {'type': type,
                        type: {
                                'type': "external",
                                'external': {'url':  url
                                            }
                                },
                        }
        return media_block
    
    # FC: [Block dict] bookmark block
    @staticmethod
    def get_bookmark_block(url:str, title:str) ->dict:
        """
        Get bookmark block dict
        
        Parameters:
            url:                    (str)       - Target block url
            title:                  (str)       - Target block title
            
        Returns:
            bookmark_block:         (dict)      - Target block dict
        """
        type = 'bookmark'
        bookmark_block = {'type': type,
                        type: {
                                'url': url,
                                },
                        }
        return bookmark_block
    
    # FC: [Block dict] equation block
    @staticmethod
    def get_equation_block(text:str) ->dict:
        """
        Get equation block dict
        
        Parameters:
            text:                   (str)       - Target block text
            
        Returns:
            equation_block:        (dict)      - Target block dict
            
        Raises:
            Exception:              (Exception) - Parameter error
        """
        type = 'equation'
        equation_block = {'type': type,
                        type: {
                                'expression': text,
                                },
                        }
        return equation_block
    
    # FC: [Block dict] divider block
    @staticmethod
    def get_divider_block() ->dict:
        """
        Get divider block dict
        
        Returns:
            divider_block:         (dict)      - Target block dict
            
        Raises:
            Exception:              (Exception) - Parameter error
        """
        type = 'divider'
        divider_block = {'type': type,
                        type: {},
                        }
        return divider_block
    
    # FC: [Block dict] table of contents block
    @staticmethod
    def get_table_of_contents_block(color:str="default") ->dict:
        """
        Get table of contents block dict
        
        Parameters:
            color:                  (str)       - Target block color
            
        Returns:
            table_of_contents_block:(dict)      - Target block dict
            
        Raises:
            Exception:              (Exception) - Parameter error
        """
        if not Dict_Gadget.check_text_color(color):
            raise Exception(f"{sys._getframe().f_code.co_name}: " +
                            "Parameter error, please check the parameter. " +
                            "'color' is not in COLOR_LIST. \n" +
                            f"COLOR_LIST = {TEXT_COLOR_LIST}")
        type = 'table_of_contents'
        table_of_contents_block = {'type': type,
                                    type: {
                                            'color': color,
                                            },
                                    }
        return table_of_contents_block
    
    # FC: [Block dict] breadcrumb block
    @staticmethod
    def get_breadcrumb_block() ->dict:
        """
        Get breadcrumb block dict
        
        Returns:
            breadcrumb_block:      (dict)      - Target block dict
        """
        type = 'breadcrumb'
        breadcrumb_block = {'type': type,
                            type: {},
                            }
        return breadcrumb_block
    
    # FC: [Block dict] column_list block
    @staticmethod
    def get_column_list_block(children:list=[]) ->dict:
        """
        Get column_list block dict
        
        Parameters:
            children:               (list)      - Target block children
        
        Returns:
            column_list_block:      (dict)      - Target block dict
        """
        type = 'column_list'
        column_list_block = {'type': type,
                            type: {'children': children},
                            }
        return column_list_block
    
    # FC: [Block dict] column block
    @staticmethod
    def get_column_block(children:list=[]) ->dict:
        """
        Get column block dict
        
        Parameters:
            children:               (list)      - Target block children
            
        Returns:
            column_block:           (dict)      - Target block dict
        """
        type = 'column'
        column_block = {'type': type,
                        type: {'children': children},
                        }
        return column_block
    
    # FC: [Block dict] link preview block
    @staticmethod
    def get_link_preview_block(url:str) ->dict:
        """
        Get link preview block dict
        
        Parameters:
            url:                  (str)       - Target block url
        
        Returns:
            link_preview_block:   (dict)      - Target block dict
        
        """
        type = 'link_preview'
        link_preview_block = {'type': type,
                            type: {'url': url},
                            }
        return link_preview_block
    
    # FC: [Block dict] template block
    @staticmethod
    def get_template_block(template_title:str, **kwargs) ->dict:
        """
        Get template block dict
        
        Returns:
            template_block:        (dict)      - Target block dict
            
        Raises:
            Exception:             (Exception) - Parameter error
        """
        type = 'template'
        
        template_title_text = {'text': {'content': template_title}}
        if 'style' in kwargs:
            template_title_text.update({'annotations':kwargs['style']})
        else:
            template_title_text.update({'annotations':Property_gadget.set_text_style(**kwargs)})
            
        template_block = {'type': type,
                          type:{'rich_text': [template_title_text]},
                        }
        if "children" in kwargs:
            if type(kwargs["children"]) is list:  # type: ignore "kwargs["children"] need be is list"
                template_block[type].update({'children': kwargs["children"]})
            else:
                raise Exception(f"{sys._getframe().f_code.co_name}: " +
                                "Parameter error, please check the parameter. " +
                                "'children' is not a list.")
            
        return template_block
    
    # FC: [Block dict] link to page block
    @staticmethod
    def get_link_to_page_block(page_id:str) ->dict:
        """
        Get link to page block dict
        
        Parameters:
            page_id:               (str)       - Target block page id
        
        Returns:
            link_to_page_block:    (dict)      - Target block dict
        """
        type = 'link_to_page'
        link_to_page_block = {'type': type,
                              type: {
                                  'type': "page_id",
                                  'page_id': page_id},
                            }
        return link_to_page_block
    
    # FC: [Block dict] link to database block
    @staticmethod
    def get_link_to_database_block(database_id:str) ->dict:
        """
        Get link to page block dict
        
        Parameters:
            page_id:               (str)       - Target block page id
        
        Returns:
            link_to_page_block:    (dict)      - Target block dict
        """
        type = 'link_to_page'
        link_to_page_block = {'type': type,
                              type: {
                                  'type': "database_id",
                                  'page_id': database_id},
                            }
        return link_to_page_block
        
    # FC: [Block dict] synced block
    @staticmethod
    def get_synced_block(children:list=[]) ->dict:
        """
        Get synced block dict
        
        Parameters:
            children:               (list)      - Target block children
        
        Returns:
            synced_block:           (dict)      - Target block dict
        """
        type = 'synced_block'
        synced_block = {'type': type,
                        type: {
                            'children': children},
                        }
        return synced_block
    
    # FC: [Block dict] synced from block
    @staticmethod
    def get_synced_from_block(block_id:str) ->dict:
        """
        Get synced from block dict
        
        Parameters:
            children:               (list)      - Target block children
        
        Returns:
            synced_from_block:      (dict)      - Target block dict
        """
        type ='synced_block'
        synced_from_block = {'type': type,
                            type: {'synced_from': {"block_id": block_id}
                                    },
                            }
        return synced_from_block

class Dict_Gadget:
    Property = Property_gadget()
    Page = Page_gadget()
    Database = Database_gadget()
    Block = Block_gadget()
    
    #--------------------------[Object]--------------------------#
    # FC [Gadget]: Get Icon object
    @staticmethod
    def get_icon_dict(emoji:str) ->dict:
        return Icon(emoji=emoji).asdict()
    
    #--------------------------[Time]--------------------------#
    # FC [Gadget-Time]: Set time str
    @staticmethod
    def set_time(date:str, time:str, timezone:str) ->str:
        """
        Set time
        
        Parameters:
            date:                   (str)           - Date ex: 2021-01-01
            time:                   (str)           - Time ex: 00:00:00
            timezone:               (str)           - Target timezone ex: Asia/Tokyo
        
        """
        tz = pytz.timezone(timezone)
        tz_offset = str(datetime.datetime.now(tz))[-6:]
        return date + "T" + time + ".000" + tz_offset
    
    # FC [Gadget-Time]: Get now time str
    @staticmethod
    def get_now_time(timezone:str) ->str:
        """
        Get now time

        Returns:
            time:                   (str)           - Time ex: Asia/Tokyo
        """
        tz = pytz.timezone(timezone)
        tz_offset = str(datetime.datetime.now(tz))[-6:]
        now_time = time.strftime("%Y-%m-%dT%H:%M:%S.000", time.localtime(time.time()))
        return now_time + tz_offset
    
    # FC [Gadget-Time]: Timezone change
    @staticmethod
    def timezone_change(utc_time:str, timezone:str) ->str:
        """
        UTC time change to timezone time

        Parameters:
            utc_time:               (str)           - UTC time
            timezone:               (str)           - Target timezone
        
        returns:
            timezone_time:          (str)           - Timezone time
        """
        tz = pytz.timezone(timezone)
        date_temp = "%Y-%m-%d"; time_temp = "%H:%M:%S"
        time_utc = datetime.datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
        time_tz = time_utc.astimezone(tz)
        return time_tz.strftime(date_temp +" "+ time_temp)

    #--------------------------[URL]--------------------------#
    # FC [Gadget-URL]: Notion Url to short_url
    @staticmethod
    def get_notion_short_url(url:str) ->str:
        """
        Get notion short url
        
        Parameters:
            url:                    (str)           - Target url

        Returns:
            result:                 (str)           - Result
        """
        return '/' + get_id(url).replace('-','')
    
    #--------------------------[Check]--------------------------#
    # FC [Gadget-Check]: Is Notion url
    @staticmethod
    def is_notion_url(url:str) ->bool:
        """
        Check if the url is a notion url
        
        Parameters:
            url:                   (str)          - Target url

        Returns:
            result:                 (bool)          - Result
        """
        if url is None:
            return False
        return url[:22] == "https://www.notion.so/"

    # FC: [Gadget-Check] text color
    @staticmethod
    def check_text_color(color:str) ->bool:
        """
        Check text color
        
        Parameters:
            color:                  (str)           - Target color

        Returns:
            result:                 (bool)          - Result
        """
        return color in TEXT_COLOR_LIST
    
    # FC: [Gadget-Check] rollup function
    @staticmethod
    def check_rollup_function(function:str) ->bool:
        """
        Check rollup function
        
        Parameters:
            function:               (str)           - Target function

        Returns:
            result:                 (bool)          - Result
        """
        return function in ROLLUP_FUNCTION_LIST
    
    # FC: [Gadget-Check] block type
    @staticmethod
    def check_block_type(type:str) ->bool:
        """
        Check block type
        
        Parameters:
            type:                   (str)           - Target type

        Returns:
            result:                 (bool)          - Result
        """
        return type in BLOCK_TYPE_LIST
    
    # FC: [Gadget-Check] code language
    @staticmethod
    def check_code_language(language:str) ->bool:
        """
        Check code language
        
        Parameters:
            language:               (str)           - Target language

        Returns:
            result:                 (bool)          - Result
        """
        return language in CODE_LANGUAGE_LIST
    
    # FC: [Gadget-Check] media type
    @staticmethod
    def check_media_type(type:str) ->bool:
        """
        Check media type
        
        Parameters:
            type:                   (str)           - Target type

        Returns:
            result:                 (bool)          - Result
        """
        return type in MEDIA_TYPE_LIST
    
    # FC: [Gadget-Check] is page dict
    @staticmethod
    def is_page(page:dict) ->bool:
        """
        Check if the page is a page
        
        Parameters:
            page:                   (dict)          - Target page

        Returns:
            result:                 (bool)          - Result
        """
        return is_full_page(page)
    
    # FC: [Gadget-Check] is database dict
    @staticmethod
    def is_database(database:dict) ->bool:
        """
        Check if the database is a database
        
        Parameters:
            database:               (dict)          - Target page

        Returns:
            result:                 (bool)          - Result
        """
        return is_full_database(database)
    
    # FC: [Gadget-Check] check dict is page or database
    @staticmethod
    def check_dict_type(dict:dict) ->str:
        """
        Check dict type
        
        Parameters:
            dict:                   (dict)          - Target page

        Returns:
            result:                 (str)           - Result page or database
        """
        if dict['object'] == 'page':
            return 'page'
        elif dict['object'] == 'database':
            return 'database'
        else:
            return 'none'
