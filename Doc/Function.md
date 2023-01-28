<!--  Database  -->

### API
- Database
  - Create a new database
  - Retrieve databse [Get page list in database]
  - Query database [Get database data]
  - Properties
    - Create property
    - Update property
    - Rename property
    - Delete property

<!--  Page  -->
- Page
  - Retrieve page [Get page data]
  - Create page
    - in database
    - in page
  - Update page

<!--  Property  -->
- Property
  - Property support: [Property_Function.md](./Property_Function.md#Propertysupport)

<!--  User   -->
- User
  - Get user list
  - Retrieve User [Get user data]
  - Who am i [Get bot data]

<!--  Blokc  -->
- Block
  - Get block data
  - Get children block list
  - Add block
  - Update block
  - Del block

### Object
- Database
  - Dict to object
  - Update title
  - Add new property
  - Update property
  - Rename property
  - Del property
  - Update database object [**Any method without use object method to update object will need call this method. Because member '.Dict' is not update**]

- Page 
  - Update title
  - Update property. `Parameter: (name:string, kwargs: PropertyItem_parameter)`
  - Clear property
  - Update page object [**Any method without use object method to update object will need call this method. Because member '.Dict' is not update**]
  - Get property item. Reuten: `PropertyItem`
  - Get properties item dictionary. Return: `[{key: value},...]`


- Property type
  - Get full dict. Return: `{key: value}`
  - Get label dict. Return: `{'name':string, 'type': string, "id": string}`

- Property Item
  - Get value

- Block
  - Get block data
  - Update block
  - Update [**Any method without use object method to update object will need call this method. Because member '.Dict' is not update**]
  - Get block base data dict. [Without "created_by", "created_time", "last_edited_by", "last_edited_time", "id", "parent"]
  - Get block item dict. Return: `{type: block item}`
  - Get block id and type dict. return: `{id: string, type:string}`

- BlockList
  - Get block list