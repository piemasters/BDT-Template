# BDT Template

- [Setup Python Environment](python-setup)
- [IntelliJ Setup](intellij-setup)
- [Run Tests](run-tests)
- [Project Structure](project-structure)
- [Creating & Updating a Python Environment](python-env)


This is a template automation testing project using Python and Cucumber with
[Behave](https://behave.readthedocs.io/en/latest/).
 
You must first setup a Python Anaconda environment to use this project. 
Steps on how to do this are listed below.

To work on the project it is highly suggested that you also setup IntelliJ with the required plugins.
Steps on how to do this are also listed below.


## <a id="python-setup">Setup Python Environment</a>

1. Install Anaconda3 - Download [here](https://www.anaconda.com/download/) and select the following options:
    1. Next
    2. I Agree
    3. All Users then Next
    4. Next (Keep C:\ProgramData\Anaconda3 as the install path)
    5. Select 'Add Anaconda to the System PATH environment variable' then Install
    6. Next
    7. Finish

2. Run the following command in the same directory as the 'env_reqs.txt' file on to generate the Environment:
    - `conda create -n BDT --file env_reqs.txt`
    
3. To activate the environment run:
    - `activate BDT`

Your terminal should now display `(BDT) C:\...`


## <a id="intellij-setup">IntelliJ Setup</a>
1. Install the following plugins:
    - gherkin
    - python-ce
        
2. Select `File > Project Structure`

3. Under `Project Settings > Project > Project SDK` select `New`, then select `Python SDK`.

4. Under `Conda Environment` select the `Existing environment` radio box, then for the `Existing environment` enter the following path:
    - `C:\ProgramData\Anaconda3\envs\BDT\python.exe`


## <a id="run-tests">Running the Tests</a>
1. If you haven't already install the package:
    - `python setup.py install`
    
2. Activate the Anaconda environment:
    - `activate BDT`
    
3. To run all tests from within the project directory run:
    - `behave`
    
4. To run specific tests use tags, for example:
    - `behave tags=P1-S1-DEMO-1` 
    
Individual log files will be created for each project, as well as a general behave log. 
This can to be configured in environment.py.

5. To run the unit tests you must first build the package:
    - ```python setup.py develop```

6. Then to run each unit test run the following:
    - ```python tests\unit\<unittestname>.py```


## <a id="project-structure">Project Structure</a>
- **data** - Contains all resource files not specific to testing, i.e. schemas
- **bdt-template** - Contains all reusable source code.
    - \_\_init\_\_.py - Initialises included source code
    - example.py - Reusable source code stored in classes
- **tests** - Contains all tests
    - **features** - Contains all your feature files
        - environment.py - Contains code to run before/after features, can be configured per project
        - global_config.py - Contains all variables used by multiple projects
        - **steps** - Contains links to all steps file for each project
            - **\<project\>.py** - Contains imports for every steps file in the project
        - **\<project\>** - Contains all test code for a project
            - \<project\>_config.py - Configuration file used throughout the project
            - **\<component\>** - Contains all feature file for the component
                - **data** - Contains all test files
                    - **\<feature\>** - Contains test files for the given feature
                        - example.json - Test data file
                - **steps** - Contains all your 'Behave' step files
                    - example.py - Step file for component
                - example.feature - Feature file for component
                - messages.py - All strings used for logging in the steps code
    - **unit** - Contains all the unit tests for the main project code
        - example_test.py
        - pytest.ini


## <a id="python-env">Creating & Updating a Python Environment</a>
The following lines of code were used on Group Infra to generate the BDT Python environment: 

```
conda create --name BDT python=3.6 pip numpy
conda install matplotlib
conda install pandas
conda install -c conda-forge python-dateutil
conda install -c conda-forge jsonschema
conda install -c conda-forge jsonref
conda install -c conda-forge pywin32
conda install -c conda-forge gherkin-official
conda install -c conda-forge behave
conda install -c conda-forge pyinstaller
conda install -c conda-forge python-hdfs
conda install -c conda-forge selenium
conda install -c conda-forge jsonschema
activate BDT
conda list --explicit > env_reqs.txt
```

Links to all the libraries listed above, along with all their dependencies are saved into the `env_reqs.txt` file in the final line.
This file can be used to generate the Environment with the following command:

* `conda create -n BDT --file env_reqs.txt`

To add additional libraries to the environment:
* Activate the environment
* Install the required libraries
* Generate a new dependencies file so that the environment can be generated in the future

```
activate BDT
conda install -c conda-forge <xxx>
conda list --explicit > env_reqs.txt
```
