# %%
import os
from pprint import pprint

from notion_kit import kit as nkit
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
#    1. Get Page object
#############################################

# 1. Get Page object
page_object = nkit.Page.get_data(page_id)

# %%
#############################################
# This cell:
#    1. Set title object
#    2. Create page [Push to notion]
#############################################

# 1. Set title object
title = nobj.RichText(text=nobj.TextContent(content="new page"),
                      annotations=nobj.TextStyle(bold=True))

# 2. Create page [Push to notion]
new_page_object = nkit.Page.create_in_page(parent_page_id=page_object.id,
                                           title=title)

# %%
#############################################
# This cell:
#    1. Update title
#        1.1 Use object method
#        1.2 Use gadget method
#    2. Add Icon
#        2.1 Add icon directly to the page object
#        2.2 Use gadget method
#    3. Update page [Push to notion]
#############################################

# 1. Update title
# 1.1 Use object method
new_title = nobj.RichText(text=nobj.TextContent(content="new page 2"),
                      annotations=nobj.TextStyle(bold=True))
new_page_object.update_title(new_title)

# 1.2 Use gadget method
new_page_object = nkit.Gadget.update_page_title(page_object=new_page_object,
                                                text="new page 3",
                                                bold=True)

# 2. Add Icon
# 2.1 Add icon directly to the page object
new_page_object.icon = nobj.Icon(emoji="🐈")
new_page_object.update()
# 2.2 Use gadget method
new_page_object = nkit.Gadget.update_page_icon(page_object=new_page_object,
                                                emoji="🐕")

# 3. Update page [Push to notion]
new_page_object = nkit.Page.update(new_page_object)


