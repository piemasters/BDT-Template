Feature: PROJECT2 A demonstration feature file
    In order to demonstrate the project functionality
    I want to provide some demo scenarios

    @P2 @P2-S1 @P2-S1-DEMO @P2-S1-DEMO-1
    Scenario Outline: A valid XML file is converted to JSON that meets the provided schema
        Given I have a file <file_name> that is xml with ID <file_id>
        When this <file_name> is copied into the ingest directory
        Then a converted JSON file is copied into the target directory
        And validates correctly against the schema <schema>
        And all key values match the expected values <test_file_expected>
        Examples: Valid files
            | file_id           | file_name         | schema            | test_file_expected  |
            | P2-S1-DEMO-1  	| P2_S1_DEMO_1.xml  | DEMO_SCHEMA.json  | P2_S1_DEMO_1.json   |

