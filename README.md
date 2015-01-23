## So you want to test? <br>
### A breakdown of a full Python testing stack
*Updated January, 2015* <br>
Below is a layer-by-layer breakdown of how I test my Python projects, starting with my Github repository and ending with the test files themselves.

## Layer 1: Travis-CI
www.Travis-CI.org

To integrate your project with Travis, go to the Travis website and log in with your Github credentials. 

***Requires these files*** <br>
- .travis.yml

Testing begins with Travis-CI, which hooks into your Github repository to automatically run tests on pull requests and current production branches. It provides a nice visual representation of when tests are failing and a decent overview of all the tests scheduled to run. Travis integration is run through a `.travis.yml` configuration file in the main project repository. Although Travis is itself a capable test runner, it is important to maintain the ability to run tests locally without having to submit a pull request to test. That's why we'll be using Tox as our test runner.

## Layer 2: Tox
http://tox.readthedocs.org/en/latest/index.html

***To install*** <br>
`pip install tox`

***To run tests locally*** <br>
(From the project directory) <br>
`tox` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Runs all tests* <br>
`tox -e py27` &nbsp;&nbsp; *Runs a single test from the testing suite (specifically the* py27 *env)*

***Requires these files*** <br>
- tox.ini
- setup.py

We use Tox as our test runner to manage all of our tests. It will be run by Travis, however it can also be run locally to test your code before it is pushed to Github. Tox requires two different files in the project directory to run. The `tox.ini` file contains all of the testing setttings and configurations. The `setup.py` file is used for supplying metadata about the project. Optionally, you can create a method within the `setup.py` file to run Tox using the traditional `python setup.py test` call from the command line. However, this adds an unnecessary step.

The tox.ini file defines the tests to run. Tox has two methods of running a test: <br>
**a)** The `[testenv]` settting

**b)** The `[testenv:mytest]` setting  --> With "mytest" listed in the `envlist` list at the top of the .ini file.

In case **(b)**, you define one python version and some commands to run. The setting needs the `[testenv:` prefix. We'll run one of these for flake8. You can create as many of these "generated" environments as you want. 

In case **(a)**, the same test is run through all non-specific environments listed in the `envlist` at the top of the .ini file. It looks like you are only allowed one `[testenv]` and have to run your whole testing suite through its commands string. 
What's pretty cool is that the way to fully test all permutations of dependencies is to generate an n*m matrix of dependencies - like testing different python versions across different django versions. 

So, you get unlimited "generated" environments, but only one main testing environment *testenv*. However, you can run different combinations of dependencies with that main *testenv*, which makes it very powerful.

 
## Layer 3: flake8
http://flake8.readthedocs.org/en/2.2.3/

Flake8 is a linter that we use to check for code style and small syntax errors. We run flake8 in its own testing environment through Tox.

Flake8 will be installed through the Tox testing environment, however we can run it separately by installing `pip install flake8` and running `flake8 directory_to_check`. The setup.cfg file can be used to change certain settings and rules of the linter.

**Note:** If flake8 catches any syntax problems, Tox will throw an `InvocationError`. Once flake8 issues are resolved, that message will go away.


## Layer 4: coverage
https://pypi.python.org/pypi/coverage

The Coverage module records the test coverage as different tests are run. We run it through the wrapper function `coverage_wrapper.py` in the main `[testenv]` testing environment through Tox. The wrapper is used to ensure that file inheritance works out well. Make sure that each directory in the project (including the tests folder) has a `__init__.py` file in it. The wrapper runs tests through the `pytest` module.


## Layer 5: pytest
https://pytest.org

Pytest is invoked through `coverage_wrapper.py` and installed on the Tox testing environment. We can run it separately by installing `pip install pytest` and running `py.test` from the project directory. Pytest crawls through the current directory, finding and running any test scripts with the filename prefix of `test_`, such as `test_mypyogram.py`. It's a good idea to keep all tests in a testing directory. 

***Requires these files*** <br>
- setup.cfg

It's important to include the following lines in your setup.cfg file to exclude unwanted directories from testing:

```
[pytest]
addopts = --verbose
# Pytest searches for test files (prefixed "test_"). Ignore these directories
norecursedirs = .tox .git env
```


---
---

## Best practices
#### Testing in Windows
Things are easier in Unix. However, if you find yourself using the Windows command line, you may notice that python modules are difficult to run. To run a python module (like Tox), try this:

`python -m tox`<br>
or to install tox: <br>
`python -m pip install tox` <br>
or to update tox: <br>
`python -m pip -U install tox`

#### `__init__.py`
Make sure a blank `__init__.py` file is in each directory, including your test directory!

#### Create virtual environment for running
*If `virtualenv` is not installed, run `pip install virtualenv`*

Navigate to the main project directory and run: <br>
Unix: `python virtualenv env` <br>
Windows: `python -m virtualenv env`

#### Use the virtual environment
Unix: 
`source env/bin/activate`

Windows: 
`env\Scripts\activate.bat`

This will temporarily change the python installation so the current command line instance uses the virtual environment. You can test your current python instance by running `which python` in Unix, or `where python` in Windows.

## Helpful Links
- http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/
- http://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
- http://jeffknupp.com/blog/2014/02/04/starting-a-python-project-the-right-way/
- http://stackoverflow.com/questions/14132789/python-relative-imports-for-the-billionth-time
- http://www.mediawiki.org/wiki/Continuous_integration/Tutorials/Test_your_python
