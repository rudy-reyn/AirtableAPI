# 02/21/22
# tests.py
import pytest
import json
import requests
from airtable import Airtable

@pytest.fixture
def workspace():
    with Airtable("base_id", "key") as ws:
        yield ws

@pytest.fixture
def with_enforce_schema():
    with Airtable("base_id", "key", enforce_schema=True) as ws:
        yield ws

def test_airtable_not_found_response(workspace):
    response = workspace.get("invalid_table")
    assert response.json() == {'error': 'NOT_FOUND'}

def test_enforce_schema(with_enforce_schema):
    with pytest.raises(ValueError):
        with_enforce_schema._request(requests.get, "invalid_table")

def test_raises_max_tables(workspace):
    with pytest.raises(ValueError):
        arguments = {"table": "invalid_table", "data": range(10), "maximum": float("-inf")}
        workspace._update_request(requests.post, **arguments)
        workspace.post("invalid_table", **arguments)

def test_raises_for_status(workspace):
    with pytest.raises(requests.HTTPError):
        workspace._request(requests.get, "invalid_table", raise_for_status=True)

def test_post_request_data(workspace):
    data = {"field1": [1, 2, 3], "field2": ["a", "b", "c"]}
    response = workspace.post("invalid_table", data=data)
    assert response.request.body == json.dumps({"records": [{"fields": i} for i in data]})

@pytest.fixture
def expected_delete_path(workspace):
    def helper(IDs):
        if isinstance(IDs, str):
            expected_path = f"/v0/base_id/invalid_table?records%5B%5D={IDs}"
        else:
            expected_path = "/v0/base_id/invalid_table?" + "&".join(f"records%5B%5D={i}" for i in IDs)
        response = workspace.delete("invalid_table", IDs=IDs)
        return response.request.path_url == expected_path
    return helper

def test_delete_request_multiple_IDs(expected_delete_path):
    assert expected_delete_path(["1", "2", "3"])

def test_delete_request_single_ID(expected_delete_path):
    assert expected_delete_path("some_record_ID")
