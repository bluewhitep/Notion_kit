# %%
import os
from pprint import pprint

from notion_kit import Kit as nkit
from notion_kit import object as nobj

# %%
#############################################
# This cell:
#    1. Read token(*) from os environment variable
#    * Following the instruction for get token:
#        https://developers.notion.com/docs/authorization#set-up-the-auth-flow-for-a-public-integration
#############################################

# 1. Recommend: use environment variable
token = os.environ["NOTION_TOKEN"]

# %%
#############################################
# This cell:
#    1. Set client
#    2. Get id from notion url
#############################################

# 1. Set client
notion_client = nkit.Client(token=token)

# 2. Get id from notion url
##   Page url
page_url = ""
page_id = nkit.get_id(url=page_url)

print("Page id: ", page_id)

# %%
#############################################
# This cell:
#    1. Shows what properties you can create and non-creatable in the database
#        - Create this properties
#############################################

# 1. Get "Creatable property list" and "Non-creatable property list" form notion_kit.CONTENTS
from notion_kit.CONTENTS import (
    ALL_PROPERTIES_TYPES,
    NON_CREATEABLE_PROPERTIES_TYPES,
)

## Get creatable property list
creatable_properties_types = list(set(ALL_PROPERTIES_TYPES) - set(NON_CREATEABLE_PROPERTIES_TYPES))
print(f"Creatable property type:\n{creatable_properties_types}")
creatable_properties_types.append("status") # Add status
print("="*20)

## Get creatable properties name
creatable_properties_names = [_.capitalize() for _ in creatable_properties_types]
print(f"Creatable property name:\n {creatable_properties_names}")

## Dict of creatable properties. Following: {name: type}
creatable_properties = dict(zip(creatable_properties_names, creatable_properties_types))

# %%
#############################################
# This cell:
#    1. Set title object: Test Database
#    2. Add properties
#        - Use "creatable_properties" from above cell
#    3. Create database [Push to notion]
#############################################

# 1. Database Name: Test DataBase
title = nobj.RichText(text=nobj.TextContent(content="Test Database"),
                      annotations=nobj.TextStyle(bold=True))

# 2. Properties list
creatable_properties_object_list = []
for name, type in creatable_properties.items():
    if type == "relation":
        relation_database_id = nkit.get_id("https://www.notion.so/73350fed70e144219b073cff9cdcc9e7?v=05938573f62c4bfbab5a1fa286761be7&pvs=4")
        database_relation = nobj.RelationSingle(database_id=relation_database_id)
        creatable_properties_object_list.append(nobj.PropertyType(name=name, type=type, relation=database_relation))
    else:
        creatable_properties_object_list.append(nobj.PropertyType(name=name, type=type))

# 3. Create database  [Push to notion]
database_object = nkit.Database.create(parent_page_id=page_id, 
                                        title=title,
                                        properties_type_list=creatable_properties_object_list,
                                        icon=nobj.Icon(emoji="📚"),
                                        is_inline=True)

# %%
#############################################
# This cell:
#    1. Show database property list
#    2. Show database object
#############################################
database_property_list = database_object.property_list()
pprint(database_property_list)
print("="*20)
pprint(database_object)

# %%
#############################################
# This cell:
#    1. Add new property to database
#        |name        |type     |
#        |------------|---------|
#        |checkbox1   |checkbox | * Use gadget method
#        |Percent     |percent  | * Use object
#    2. Update property
#        - select, multi_select: add new option
#            |name        |color     |
#            |------------|----------|
#            | A          |'default' |
#            | B          |'red'     |
#            | C          |'green'   |
#            1. Use object method add "option object" to database
#            2. Add "option object" directly to the database
#            3. Use gadget method add "option object" to database
#    3. Add status property, but it is unsupported on notion sdk
#    4. Update database [Push to notion]
#############################################

# 1. Add new property to database
# 1.1 Create new property
new_property_for_gadget = nkit.Gadget.PropertyType.get_checkbox(name="Checkbox 1")
new_property_for_object = nobj.PropertyType(name="Percent", type="number",
                                            number=nobj.Number(format="percent"))
# 1.2 Add new property to database object
database_object.properties.update(new_property_for_gadget.full_dict())
database_object.properties.update(new_property_for_object.full_dict())
# 1.3 Update database object
database_object.update()

# 2. Update property
# 2.1 Create new option
options_set = dict(zip(['A', 'B', 'C'], 
                       ['default', 'red', 'green']))
options_object = [nobj.Option(name=name, color=color) for name, color in options_set.items()]
# 2.2.1 Use object method add "option object" to database
database_object.update_property(name='Select',
                                select=nobj.Options(options=options_object))
# 2.2.2 Add "option object" directly to the database
database_object.properties['Multi_select'].multi_select = nobj.Options(options=options_object) # type: ignore
database_object.update()
# 2.2.3 Use gadget method add "option object" to database
database_object = nkit.Gadget.update_database_property(database_object=database_object,
                                                       property_name='Multi_select',
                                                       new_property=nobj.PropertyType(multi_select=nobj.Options(options=options_object)))

# 3. Add status property, but it is unsupported on notion sdk
#     - Property Name: Status 
#     - Property Type: status
#     - Property Values: ['A', 'B', 'C']
#     - Property Values Color: ['default', 'red', 'green']
status_options = [{'name': 'A', 'color': 'default', 'id':'123'},
                  {'name': 'B', 'color': 'red', 'id':'456'},
                  {'name': 'C', 'color': 'green', 'id':'789'}]
status_groups = [{'name': 'Group1', 'color': 'default', 'ids':[status_options[0]['id']]},
                  {'name': 'Group2', 'color': 'red', 'ids':[status_options[1]['id']]},
                  {'name': 'Group3', 'color': 'green', 'ids':[status_options[2]['id']]}]

status_options_object_list = [nobj.Option(name=option['name'], color=option['color'], id=option['id']) for option in status_options]
status_groups_object_list = [nobj.Group(name=group['name'], color=group['color'], option_ids=group['ids']) for group in status_groups]

database_object.properties.update({"Status":nobj.PropertyType(name="Status", type="status",
                                                            status = nobj.Status(options=status_options_object_list,
                                                                                groups=status_groups_object_list))})
database_object.update()

# 4. Update database [Push to notion]
new_database_object = nkit.Database.update(database_object)

# %%
#############################################
# This cell:
#    1. Update database title
#        1.1 Use object method
#        1.2 Use gadget method
#    2. Rename property
#        2.1 Use object method
#        2.2 Use gadget method
#    3. Delete property
#        3.1 Use object method
#        3.2 Use gadget method
#    4. Update database [Push to notion]
#############################################

# 1. Update database title
# 1.1 Use object method
new_title = nobj.RichText(text=nobj.TextContent(content="Test Database 2"))
new_database_object.update_title(new_title)
# 1.2 Use gadget method
new_database_object = nkit.Gadget.update_database_title(database_object=new_database_object,
                                                        text="Test Database 3")

# 2. Rename property
# 2.1 Use object method
new_database_object.rename_property("Checkbox", "Checkbox 2")
# 2.2 Use gadget method
new_database_object = nkit.Gadget.rename_database_property(database_object=new_database_object,
                                                           old_name="Checkbox 1",
                                                           new_name="Checkbox 3")

# 3. Delete property
# 3,1 Use object method
new_database_object.del_property("Percent")
# 3.2 Use gadget method
nkit.Gadget.del_database_property(database_object=new_database_object,
                                  property_name="Percent")

# 4. Update database [Push to notion]
new_database_object = nkit.Database.update(new_database_object)

# %%
#############################################
# This cell:
#    1. Set title of page
#    2. Init property value
#    3. Create page on database [Push to notion]
#############################################

# 1. Set title of page
page_title_obejct = nobj.RichText(text=nobj.TextContent(content="Test Page"),
                                    annotations=nobj.TextStyle(bold=True))

# 2. Init property value
# Checkbox 2 turn on
checkbox_item_object = nobj.PropertyItem(type="checkbox", checkbox=True)

# 3. Create page on database [Push to notion]        
page_obejct = nkit.Page.create_in_database(parent_database_id=new_database_object.id,
                                           properties_item_dict={"Checkbox 2":checkbox_item_object},
                                           title=page_title_obejct,
                                           icon=nobj.Icon(emoji="😀"))

# %%
#############################################
# This cell:
#    1. Show page property list of dict
#    2. Show page object
#############################################
page_property_list = page_obejct.property_list()
print("="*20)
pprint(page_obejct.Dict)

# %%
#############################################
# This cell:
#    1. Get page list of database
#############################################

# 1. Get page list of database
database_contiainer_object = nkit.Database.get_pages(database_id=new_database_object.id)

# Show
print(len(database_contiainer_object.results))
print(database_contiainer_object.results[0] == page_obejct)

# %%
#############################################
# This cell:
#    1. Update page title
#    2. Remove icon
#    3. Update page [Push to notion]
#############################################


# 1. Update page title
#    - New title: New Test page of database
#    - Text style: bold, italic
new_title_object = nobj.RichText(text=nobj.TextContent(content="New Test page of database"),
                                    annotations=nobj.TextStyle(bold=True, italic=True))

page_obejct.update_title(new_title_object)

# 2. Remove icon
page_obejct.icon = None
page_obejct.update()
                          
# 3. Update page [Push to notion]
new_page_object = nkit.Page.update(page_obejct)   

# %%
#############################################
# This cell:
#    1. Update page properties
#        1.1 Text: Hello World [bold]
#            *: Add directly to the page object
#        1.2 Number: 0.5
#            *: Use object method
#        1.3 Select: B
#            *: Use Gadget method
#    2. Update page [Push to notion]
#############################################

# 1. Update page properties
# 1.1 Text: Hello World [bold]
# *: Add directly to the page object
new_page_object.properties['Rich_text'].rich_text = [nobj.RichText(text=nobj.TextContent(content="Hello World"),
                                                                    annotations=nobj.TextStyle(bold=True))]
# 1.2 Number: 0.5
# *: Use object method
new_page_object.update_item(name='Number', number=0.5)

# 1.3 Select: B
# *: Use Gadget method
# 1.3.1 Get select option list
select_option_list = new_database_object.properties['Select'].select.get_options_list() # type: ignore
pprint(select_option_list)
# 1.3.2 Update optionty
nkit.Gadget.update_page_property(page_object=new_page_object,
                                 property_name='Select',
                                 select=nobj.Option(**select_option_list[1]))
# new_page_object.update_item(name='Select',
#                             select=nobj.Option(**select_option_list[1]))

# 2. Update page [Push to notion]
new_page_object = nkit.Page.update(new_page_object)   

# %%
#############################################
# This cell:
#    1. Clear page property
#        1.1 object method
#        1.2 gadget method
#    2. Update page [Push to notion]
#############################################

# 1. Clear page property
# 1.1 object method
new_page_object.clear_item(name='Rich_text')
# 1.2 gadget method
nkit.Gadget.clear_page_property(page_object=new_page_object,
                                property_name='Number')

# 2. Update page [Push to notion]
new_page_object = nkit.Page.update(new_page_object)   


