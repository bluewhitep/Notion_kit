[TOC]

---
# Dictionary Operation
- Change property need ```'property name'``` key or ```'id'``` key as identification label.
- Exsample：
    ```python
    {'Number': {'id': 'OVEWREGC',
                'number': {'format': 'number'},
                'type': 'number'}
    ```
  - Update property 
    - Change format
      ```python
      {'Number': {'number': {'format': 'percent'}}}
      # or
      {'OVEWREGC': {'number': {'format': 'percent'}}}
      ```
    - Change type
      ```python
      {'Number': {'Checkbox':{},
                  'type': 'Checkbox'}}
      # or
      {'OVEWREGC': {'Checkbox':{},
                  'type': 'Checkbox'}}
      ```
    - Change property name
      ```python
      {'Number': {"name": 'Number1'}}
      # or
      {'OVEWREGC': {"name": 'Number1'}}
      ```
  - Created new property
    - If dict without 'id' key and the title name is not exist this database, it will be created new property.
    ```python
    {'Number 1': {'number': {'format': 'number'}, 
                  'type': 'number'}
    ```
  - Delet Property
    ```python
    {'Number':  None}
    or
    {'OVEWREGC':  None}
    ```

## Pagebase properties update
- Quicky update properties
  - Short type of fast update page properties value
    ```python
    text_dict       = {Text title : {'rich_text': [{'text': {'content': text content}}]}}
    number          = {Number title : {'number': value}}
    checkbox        = {Checkbox title : {'checkbox': True/False}}
    multi_select    = {Multi_select title : {'multi_select': [{'name': str}, {'name': str}]}}
    select          = {Select title : {'select': {'name': str}}}
    status          = {Status title : {'status': {'name: str}}}
    title           = {Title name : {'title': [{'text': {'content': text content}}]}}
    ```

## Properites things
- Important
  - Database: ``name`` or ``id`` key is required.  Because is identification label.