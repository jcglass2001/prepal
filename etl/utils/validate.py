import json
from jsonschema import validate, exceptions
from config.settings import AppSettings
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(curr_dir)
schema_dir = os.path.join(root_dir, "schemas")


def load_schema(filename=AppSettings.SCHEMA_FILENAME) -> dict:
    schema_path = os.path.join(schema_dir, filename)

    with open(schema_path, "r") as file:
        return json.load(file)


def validate_json(data) -> None:
    schema = load_schema()
    validate(instance=data, schema=schema)
