import jsonschema
import json
from os.path import join, dirname


class JsonHandler:

    @staticmethod
    def get_json_file_contents(file):
        """ Get contents of a JSON file

        :return: The contents of a json file
        :rtype: object
        """
        with open(file, "r") as f:
            return json.loads(f.read())

    @staticmethod
    def assert_valid_json_schema(data, schema_path):
        """ Checks data against a json schema

        :param data: JSON to validate against a schema
        :param schema_path: JSON schema path
        :return: True if JSON is valid, error message if not
        """

        schema = JsonHandler.load_json_schema(schema_path)

        try:
            result = jsonschema.validate(data, schema)
        except jsonschema.exceptions.ValidationError as err:
            result = err

        return result

    @staticmethod
    def load_json_schema(schema_path):
        """ Returns a JSON schema as a JSON object

        :param schema_path: Path to schema file
        :return: JSON schema contents
        """
        # absolute_path = join(dirname(__file__), schema_path)

        with open(schema_path) as schema_file:
            return json.loads(schema_file.read())

    @staticmethod
    def compare_json(expected, actual, incorrect_fields):
        """ Compares all fields between two json objects and stores missing keys and inconsistencies in a list

        :param expected: A JSON object that contains the expected values
        :param actual: A JSON object that contains unknown values
        :param incorrect_fields: An array used to store all fields that do not match
        """
        for key in {**expected, **actual}.keys():
            # Add keys not in both to the list, marked as 'missing'
            if key not in actual or key not in expected:
                incorrect_fields.append(('missing', key))
            # If keys don't match, add primitives to the list as key/value, or use recursion for sub dictionaries/lists
            elif actual[key] != expected[key]:
                if isinstance(actual[key], dict):
                    JsonHandler.compare_json(expected[key], actual[key], incorrect_fields)
                elif isinstance(actual[key], list):
                    for index, item in enumerate(actual[key]):
                        JsonHandler.compare_json(expected[key][index], actual[key][index], incorrect_fields)
                else:
                    incorrect_fields.append((key, actual[key]))
