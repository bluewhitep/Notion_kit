# Table of Contents
* [notion_kit](#notion_kit)
* [Usage](#usage)
   * [Install](#install)
   * [Quicky start](#quicky-start)
      * [Object](#object)
* [Functions](#functions)
* [Tips](#tips)
* [Requirements](#requirements)
* [Reference](#reference)
* [License](#license)
---

# notion_kit
Is for easier use [notion-sdk-py](https://github.com/ramnes/notion-sdk-py).

- Because Notion_sdk_py Usage documentation is less, cumbersome to use, and too many dictionary operations.

- In order to make it easier to use Notion API, a lot of functions that may not be used have been created. :)


---
# Usage
## Install
- pypi
    ```bash
    pip install notion-kit
    ```
- Github
    ```bash
    pip install git+https://github.com/bluewhitep/notion_kit.git
    ```
- **Refer to the [./examples](./examples/) fold for details on usage**

## Quicky start
1. Following the instruction for get token: [Notion Authorization](https://developers.notion.com/docs/authorization)
2. Use the token. **[Recommend: Use environment variable]**
    ```python
    token = os.environ["NOTION_TOKEN"]
    ```
3. Initalize notion_kit
    ```python
    from notion_kit import kit as nkit
    notion_client = nkit.Client(token=token)
    ```
4. Get id from notion url
    ```python
    notion_url = "<Notion url>" 
    notion_id = nkit.get_id(url=notion_url)
    ```
- Get data
    ```python
    page = nkit.Page.get_data(notion_id)
    # or
    database = nkit.Database.get_data(notion_id)
    ```

### Object 
- Notion_kit use class object operations
  - object to dict
    ```python
    data_dict = data_object.Dict
    # or
    data_dict = data_object.asdict()
    ```
- Special cases:
  - ```PropertyType``` object can use ```.full_dict()``` to get ```{Property_name: Property_type_value}``` dict.
    ```python
    data_dict = data_object.full_dict()
    ```
  - ```PropertyType``` object can use ```.label_dict()``` to get short info dict.
    ```python
    data_dict = data_object.label_dict()

    # short info dict:
    # {'name': Property_name,
    #  'type': Property_type,
    #  'id': Property_id
    # }
    ```

---
# Functions
- Database
  - ⭕️ Create a new database
  - ⭕️ Retrieve databse [Get page list in database]
  - ⭕️ Query database [Get database data]
  - ⭕️ Create / Update property
  - ❌ Delete database [**Notion api not support**]
- Page
  - ⭕️ Create page in database / page
  - ⭕️ Retrieve (get page data)
  - ⭕️ Update property [ ** Page in Database]
  - ⭕️ Block [add / update / delete block]
  - ❌ Delete page [**Notion api not support**]
- Block
  - ⭕️ Create
  - ⭕️ Retrieve (get block data and block childrens)
  - ⭕️ Update (rename function from notion_sdk_py)
  - ⭕️ Delete block
- User 
  - ⭕️ Get user list
  - ⭕️ Get user data by user_id
  - ⭕️ who am i: Get bot user data

---
# Tips
### Database non-create properties
- ``status`` can't be updated, because notion api not support it.
  > By notion api document, ``title``, ``rich_text``, ``number``, ``select``, ``multi_select``, ``date``, ``people``, ``files``, ``checkbox``, ``url``, ``email``, ``phone_number``, ``formula``, ``relation``, ``rollup``, ``created_time``, ``created_by``, ``last_edited_time``, ``last_edited_by`` can be updated.
- ``rollup`` can't be updated on items.

---
# Requirements
This package supports the following minimum versions:
  - Python >= 3.10

---
# Reference
- [Notion API](https://developers.notion.com/reference/intro)
- [notion_sdk_py](https://github.com/ramnes/notion-sdk-py)

---
# License
- MIT License
