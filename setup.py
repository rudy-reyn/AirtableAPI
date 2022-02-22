from setuptools import setup

with open("README.md", "r") as md:
    long_description = md.read()

setup(
    name="Airtable Python API",
    version="0.0.1",
    author="Rudy Reynolds",
    packages=["airtable", "airtable.datatypes"],
    install_requires=[
        "requests",
        "pytest",
    ],
    author_email="rudy@rudyreynolds.dev",
    description="Simple Python wrapper around dynamically generated Airtable Workspace APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rure6748/AirtableAPI",
)
