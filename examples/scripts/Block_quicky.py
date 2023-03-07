# %%
import os
from pprint import pprint

from notion_kit.tool import Kit as nkit
from notion_kit import object as  nobj

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
#    1. Get block object
#    2. Get block children list
#############################################

# 1. Get block object
block_data_object = nkit.Block.get_data(page_id)

# 2. Get block children list
block_list_object = nkit.Block.get_children_blocks(page_id)

# %%
#############################################
# This cell:
#    1. Add block
#        1.1. Heading_1
#        1.2. Paragraph
#    2. Add block to page [Push to notion]
#############################################

# 1. Add block
# 1.1. Heading_1
#    - text: Heading 1
heading_text = nobj.Heading(rich_text=[nobj.RichText(text=nobj.TextContent(content="Heading 1"),
                                                     annotations=nobj.TextStyle(bold=False))
                                       ])
heading_1_object = nobj.Block(type="heading_1",
                                heading_1=heading_text)
# 1.2. Paragraph
#    - text: Paragraph
#    - style: bold
paragraph_text = nobj.Paragraph(rich_text=[nkit.Gadget.Object.get_rich_text(text="Paragraph", bold=True)])
paragraph_object = nobj.Block(type="paragraph",
                                paragraph=paragraph_text)

block_list = []
block_list.append(heading_1_object)
block_list.append(paragraph_object)

# 2. Add block to page [Push to notion]
new_object_list = nkit.Block.add_block(page_id, block_list)

# %%
#############################################
# This cell:
#    1. Update block
#    2. Update block to page [Push to notion]
#############################################

# Update block
## Paragraph
### Paragraph -> paragraph 2
### remove bold
block_object = new_object_list.results[1]

paragraph_object = nobj.Paragraph(rich_text=[nobj.RichText(text=nobj.TextContent(content="paragraph 2"),
                                                        annotations=nobj.TextStyle(bold=False))
                                            ])
block_object.update_block(paragraph=paragraph_object)

# 2. Update block to page [Push to notion]
new_block_object = nkit.Block.update(block_object)

# %%
#############################################
# This cell:
#    1. Delete block
#############################################

# 1. Delete block
del_block_dict = nkit.Block.del_block(block_id=new_object_list.results[0].id)


