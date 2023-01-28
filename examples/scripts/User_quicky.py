# %%
import os
from pprint import pprint

from notion_kit import kit as nkit

# %%
token = os.environ["NOTION_TOKEN"]
notion_client = nkit.Client(token=token)

# %%
# Get User list
user_list = nkit.User.get_user_list()
pprint(user_list)

# %%
# who am i
bot = nkit.User.who_am_i()
pprint(bot.Dict)

# %%
# Get user data by user_id
user_data = nkit.User.get_user_data(user_id=user_list[0].id)
pprint(user_data)


