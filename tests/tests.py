#!/usr/bin/env python3
# 02/11/22
# tests.py
# rudy@sprints
from random import choice, randint
from string import digits, ascii_lowercase as lower, ascii_uppercase as upper
import json
from airtable import AirtableAPI

with open("tests/credentials.json") as cred, open("tests/schema.json") as schem:
    base, api_key = json.load(cred).values()
    schema = json.load(schem)

def gen_random_customers(num_customers=1):
    generate = lambda a=1, b=10: choice(lower + upper)\
            + "".join(choice(lower + upper + digits) for i in range(randint(a, b)))
    def rand_cust():
        return {"firstName": generate(3, 15).title(), "lastName": generate(8, 14).title(),
                "email": f"{generate(4, 20)}@colorado.edu", "joinDate": "2022-02-11"}
    return [rand_cust() for i in range(num_customers)]

def gen_random_product(num_customers=1):
    product = connection.select("Product")
    print(f"Product Table Before:", product)
    print(json.dumps(product.json(), indent=4))
    connection.insert("Product", data={})
    connection.update("Product", data=IDs)
    print(f"Product Table After:", json.dumps(customer, indent=4))

def test_customer(connection, custs=10):
    customer = connection.select("Customer")

    print(f"Customer Table Before:", customer)
    print("Inserting test data into 'Customer' table")

    response = connection.insert("Customer", fields=gen_random_customers(custs))
    print(response.json())
    if input("Delete inserted records?: ") in ("y", "yes"):
        inserted_IDs = tuple(res["id"] for res in response.json()["records"])
        deleted = connection.delete("Customer", IDs=inserted_IDs)
        print("Deleted:", deleted.json())

def test_product(connection):
    return

def partition(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

with AirtableAPI(base, api_key, schema) as connection:
    test_customer(connection, 5)
    test_product(connection)
