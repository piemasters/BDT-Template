Feature: PROJECT1 A demonstration feature file
    In order to demonstrate the project functionality
    I want to provide some demo scenarios

    @P1 @P1-S1 @P1-S1-DEMO @P1-S1-DEMO-1
    Scenario Outline: A valid XML file is converted to JSON that meets the provided schema
        Given I have a xml input file <file_name> with ID <file_id>
        When I place this <file_name> into the ingest directory
        Then the file is converted to JSON into the correct location
        And will be valid against the schema <schema>
        And the field values match the expected output <test_file_expected>
        Examples: Valid files
            | file_id           | file_name         | schema            | test_file_expected  |
            | P1-S1-DEMO-1  	| P1_S1_DEMO_1.xml  | DEMO_SCHEMA.json  | P1_S1_DEMO_1.json   |

