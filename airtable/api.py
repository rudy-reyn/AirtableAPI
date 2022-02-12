# 02/11/22
# app.py
from typing import Optional
import json
import requests
from requests import Session
from .utils import require

class AirtableBaseAPI:
    def __init__(self, base, api_key, schema: Optional[dict]=None):
        self.host = "https://api.airtable.com/v0"
        self.base = base
        selAirtableAPIy = api_key
        self.schema = schema
        self.api = f"{self.host}/{base}"
        self.auth = {"Authorization": f"Bearer {api_key}"}
        self.session = Session()

    def _request(self, method, table, *args, headers=None, raise_for_status=False, **kwargs):
        require(self._validate_tables_exist(table), ValueError(f"Table {table} does not exist"))
        headers = headers or {}
        response = method(f"{self.api}/{table}", *args, headers=self.auth | headers, **kwargs)
        if raise_for_status:
            response.raise_for_status()
        return response

    def _update_request(self, method, table, data, *args, headers=None, **kwargs):
        headers = {"Content-Type": "application/json", **(headers or {})}
        return self._request(method, table, *args, headers=headers, data=json.dumps(data), **kwargs)

    def _validate_tables_exist(self, *tables):
        if not self.schema:
            return True
        return all(table in self.schema["tables"] for table in tables)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

class AirtableAPI(AirtableBaseAPI):
    @staticmethod
    def _validate_update_length(values, maximum=10):
        require(0 < len(values) <= maximum,  TypeError("Only between one and ten values can be included."))

    def select(self, table, *args, **kwargs):
        return self._request(self.session.get, table, *args, **kwargs)

    def insert(self, table, fields, *args, **kwargs):
        self._validate_update_length(fields)
        data = {"records": [{"fields": i} for i in fields]}
        return self._update_request(self.session.post, table, data, *args, **kwargs)

    def update(self, table, data, **kwargs):
        self._validate_update_length(data)
        return self._update_request(self.session.patch, table, data, *args, **kwargs)

    def update_and_clear(self, table, data, **kwargs):
        self._validate_update_length(data)
        return self._update_request(self.session.put, table, data, *args, **kwargs)

    def delete(self, table, *, ID=None, IDs=None, **kwargs):
        require((not ID) ^ (not IDs), ValueError("Only one of ID and IDs can be specified at a time."))
        if ID:
            require(isinstance(ID, str), TypeError(f"ID must be of type 'str', got: '{type(str)}'"))
            return self._request(self.session.delete, table, params={"records[]", ID}, **kwargs)
        else:
            self._validate_update_length(IDs)
            params = [(f"records[]", ID) for ID in IDs]
            return self._request(self.session.delete, table, params=params, **kwargs)

    def dump_tables(self, tables=(), **kwargs):
        for table in tables or self.schema["tables"]:
            response = self.session.get(table, **kwargs)
            yield table, response.json()
