# %%
import os
from pprint import pprint

from notion_kit import Kit as nkit

# %%
token = os.environ["NOTION_TOKEN"]
notion_client = nkit.Client(token=token)

# %%
page_url = ""

database_url = ""

database_page_url = ""


# %%
# Show page object
page_object = nkit.Page.get_data(nkit.get_id(page_url))

pprint(page_object)

# %%
# Show database object
database_object = nkit.Database.get_data(nkit.get_id(database_url)) 

pprint(database_object.Dict)

# %%
# Show database container object
database_pages_object = nkit.Database.get_pages(nkit.get_id(database_url)) 

pprint(database_pages_object)

# %%
# Show page object
page_on_database_object = nkit.Page.get_data(nkit.get_id(database_page_url))

pprint(page_on_database_object)


