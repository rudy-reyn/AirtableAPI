# 02/11/22
# app.py
from typing import Optional, Generator
import json
import requests
from requests import Session, Response

class AirtableBaseAPI:
    def __init__(self, baseID, api_key, tables: dict):
        self.host = "https://api.airtable.com/v0"
        self.base = baseID
        selAirtableAPIy = api_key
        self.tables = tables
        self.api = f"{self.host}/{baseID}"
        self.auth = {"Authorization": f"Bearer {api_key}"}
        self.session = Session()

    def _request(self, method, table, *args, headers=None, raise_for_status=False, **kwargs) -> Response:
        if not self._validate_tables_exist(table):
            raise ValueError(f"Table {table} does not exist")
        headers = headers or {}
        response = method(f"{self.api}/{table}", *args, headers=self.auth | headers, **kwargs)
        if raise_for_status:
            response.raise_for_status()
        return response

    def _update_request(self, method, table, data, *args, headers=None, **kwargs) -> Response:
        headers = {"Content-Type": "application/json", **(headers or {})}
        return self._request(method, table, *args, headers=headers, data=json.dumps(data), **kwargs)

    def _validate_tables_exist(self, *tables):
        return all(table in self.tables for table in tables)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

class Airtable(AirtableBaseAPI):
    @staticmethod
    def _validate_update_length(values, maximum=10):
        if not 0 < len(values) <= maximum:
            raise TypeError("Only between one and ten values can be included.")

    def select(self, table, *args, **kwargs) -> Response:
        return self._request(self.session.get, table, *args, **kwargs)

    def insert(self, table, records, *args, **kwargs) -> Response:
        self._validate_update_length(records)
        data = {"records": [{"fields": i} for i in records]}
        return self._update_request(self.session.post, table, data, *args, **kwargs)

    def update(self, table, data, *args, **kwargs) -> Response:
        self._validate_update_length(data)
        return self._update_request(self.session.patch, table, data, *args, **kwargs)

    def update_and_clear(self, table, data, *args, **kwargs) -> Response:
        self._validate_update_length(data)
        return self._update_request(self.session.put, table, data, *args, **kwargs)

    def delete(self, table, *, ID=None, IDs=None, **kwargs) -> Response:
        if not (not ID) ^ (not IDs):
            raise ValueError("Only one of ID and IDs can be specified at a time.")
        if ID:
            if not isinstance(ID, str):
                raise TypeError(f"ID must be of type 'str', got: '{type(str)}'")
            return self._request(self.session.delete, table, params={"records[]", ID}, **kwargs)
        else:
            self._validate_update_length(IDs)
            params = [(f"records[]", ID) for ID in IDs]
            return self._request(self.session.delete, table, params=params, **kwargs)

    def dump_tables(self, tables=(), *args, **kwargs) -> Generator:
        for table in tables or self.tables:
            yield table, self.select(table, *args, **kwargs)
