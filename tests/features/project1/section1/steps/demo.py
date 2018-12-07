from behave import *

from tests.features.project1 import project1_config as config
import tests.features.project1.section1.messages as messages
from bdt_template import FileManager, JsonHandler, TimeManager, LoggingManager


@given('I have a xml input file {file_name} with ID {file_id}')
def step_impl(context, file_name, file_id):
    # Make the id available to future steps
    context.file_id = file_id

    # Ensure each test file exists
    assert (FileManager.file_exists(config.TEST_DATA_DEMO + file_name))


@when('I place this {file_name} into the ingest directory')
def step_impl(context, file_name):
    # Copy test file to the XML ingest directory and ensure it has been copied directly
    FileManager.copy_file(config.TEST_DATA_DEMO + file_name, config.XML_INGEST + file_name)

    # Used to simulate another system ingesting the file and converting it in the output dir
    FileManager.copy_file(config.TEST_DATA_DEMO + 'P1_S1_DEMO_1.json', config.JSON_OUTPUT + 'P1_S1_DEMO_1.json')

    assert (FileManager.file_exists(config.XML_INGEST + file_name))


@then('the file is converted to JSON into the correct location')
def step_impl(context):
    # Expected & error directories
    expected_dir = config.JSON_OUTPUT
    error_dirs = [config.ERROR_OUTPUT, config.FAILURE_OUTPUT]
    scan_dirs = [expected_dir] + error_dirs

    # Watch all output directories for the file for 2 minutes and get the matched file
    matched_file, file_found_dir = FileManager.scan_dirs(context.file_id, scan_dirs, 'contents')
    context.matched_file = matched_file

    # Log the correct message
    if file_found_dir == expected_dir:
        LoggingManager.bdt_logger('INFO', context.file_id, messages.P1_S1_DEMO_1_EXPECTED, matched_file)
    elif file_found_dir in error_dirs:
        LoggingManager.bdt_logger('ERROR', context.file_id, messages.P1_S1_DEMO_1_ERROR, matched_file, open(matched_file).readline())
    else:
        LoggingManager.bdt_logger('ERROR', context.file_id, messages.P1_S1_DEMO_1_UNKNOWN)

    assert file_found_dir == expected_dir


@then('will be valid against the schema {schema}')
def step_impl(context, schema):

    # Get contents of matched file
    data = JsonHandler.get_json_file_contents(context.matched_file)

    # Validate the file contents against the schema
    schema_result = str(JsonHandler.assert_valid_json_schema(data, config.TEST_DATA_DEMO + schema))
    expected_schema_result = 'None'

    # Log the correct message
    if schema_result == expected_schema_result:
        LoggingManager.bdt_logger('INFO', context.file_id, messages.P1_S1_DEMO_2_EXPECTED, context.matched_file)
    else:
        LoggingManager.bdt_logger('ERROR', context.file_id, messages.P1_S1_DEMO_2_ERROR, context.matched_file, schema_result)

    assert schema_result == expected_schema_result


@then('the field values match the expected output {expected_output}')
def step_impl(context, expected_output):
    # Get the contents of the matched file and expected test file
    actual_data = JsonHandler.get_json_file_contents(context.matched_file)
    expected_data = JsonHandler.get_json_file_contents(config.TEST_DATA_DEMO + expected_output)

    # Compare actual & expected results and create a list of all non-matching fields
    incorrect_fields = []
    JsonHandler.compare_json(expected_data, actual_data, incorrect_fields)

    # For each non-matching field, ignore auto-generated timestamps generated in the last 10mins
    unresolved_conflicts = []
    dynamically_generated_keys = ['timestamp']
    for key, value in incorrect_fields:
        if key in dynamically_generated_keys:
            if not TimeManager.check_timestamp_recent(value, 10):
                unresolved_conflicts.append((key, value))
        else:
            unresolved_conflicts.append((key, value))

    # Log the correct message
    if len(unresolved_conflicts) == 0:
        LoggingManager.bdt_logger('INFO', context.file_id, messages.P1_S1_DEMO_3_EXPECTED, context.matched_file)
    else:
        LoggingManager.bdt_logger('ERROR', context.file_id, messages.P1_S1_DEMO_3_ERROR, context.matched_file, str(unresolved_conflicts))

    assert not unresolved_conflicts
