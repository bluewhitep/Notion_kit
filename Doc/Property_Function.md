# Property type support

   Properties Type   | Create | Rename | Update Value | Update options | Delete 
:-------------------:|:------:|:------:|:------------:|:--------------:|:------:
 checkbox            | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 created_by          | ⭕️     | ⭕️     | ❌            | ❌              |   ⭕️
 created_time        | ⭕️     | ⭕️     | ❌            | ❌              |   ⭕️
 date                | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 email               | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 files               | ⭕️     | ⭕️     | ⭕️[Limted]    | ❌              |   ⭕️
 formula             | ⭕️     | ⭕️     | ❌            | ❌              |   ⭕️
 last_edited_by      | ⭕️     | ⭕️     | ❌            | ❌              |   ⭕️
 last_edited_time    | ⭕️     | ⭕️     | ❌            | ❌              |   ⭕️
 multi_select        | ⭕️     | ⭕️     | ⭕️            | ⭕️              |   ⭕️
 number              | ⭕️     | ⭕️     | ⭕️            | ⭕️              |   ⭕️
 people              | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 phone_number        | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 relation            | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 rich_text           | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 rollup              | ⭕️     | ⭕️     | ⭕️[Limted]    | ❌              |   ⭕️
 select              | ⭕️     | ⭕️     | ⭕️            | ⭕️              |   ⭕️
 status              | ❌     | ⭕️     | ❌            | ❌              |   ⭕️
 title               | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️
 url                 | ⭕️     | ⭕️     | ⭕️            | ❌              |   ⭕️

- files:
  - only support ```delete files``` and ```pass files```.
  > Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion, it remains one of the files.
 
- rollup:
  - only support **get rollup items**. [Can't support create, update]