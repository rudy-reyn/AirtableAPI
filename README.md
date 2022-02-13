# Python Airtable API

## Overview
[Airtable](https://airtable.com) is a web based data management tool that allows users to store and
manipulate data, connect with existing applications, and publish views to external websites.
Projects containing related tables and applications are stored in Workspaces. Airtable dynamically
generates easy to use [REST APIs](https://airtable.com/api) and documentation for each Workspace.

This is a Python wrapper for interacting with Workspace APIs, allowing for GET, POST, PATCH, and
DELETE requests based on each field.

## Usage
```python3
import requests
from airtable import Airtable

# Airtable(baseID: str, api_key: str, schema: dict)
baseID, api_key = "YOUR WORKSPACE BASE ID", "API KEY"
schema = {"Table 1": {"field1"}}

with Airtable(baseID, api_key, schema) as workspace:
    # Select all records from Table 1
    selected: requests.Response = workspace.select("Table 1")

    # Insert records into a specified table
    records =  [{"field1": 10}, {"field1": 2}]
    insert: requests.Response = workspace.insert("Table 1", records=records)

    if insert.ok:
        print(insert.json())

    # Returns ->
    # {
    #     "records": [
    #        {
    #             "id": "rec3YdOPShcluFVg6",
    #             "fields": {"field1": 10},
    #             "createdTime": "2022-02-11T00:27:33.000Z"},
    #        {
    #             "id": "recIJmn0jfRUNKvSk",
    #             "fields": {"field1": 2},
    #             "createdTime": "2022-02-11T00:27:33.000Z"}
    #     ]
    # }

    # Delete inserted records
    delete = [i["id"] for i in insert.json()["records"]]
    deleted: requests.Response = workspace.delete("Table 1", IDs=delete)

    if deleted.ok:
        print(deleted.json())

    # Returns ->
    # {
    #     "records": [
    #         {
    #             "id": "rec3YdOPShcluFVg6",
    #             "deleted": true
    #         },
    #         {
    #             "id": "recIJmn0jfRUNKvSk",
    #             "deleted": true
    #         }
    #     ]
    # }

```
