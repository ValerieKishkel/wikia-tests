# Wikia Selenium Tests #

## Installation ##

### Requirements: ###
* Python 2.7 + pip or easy_install
* Firefox
* Chrome + chromedriver

### Prepare Virtual Environment: ###
You can use your existing one or create a new one using `virtual-env` or `mkvirtualenv`

Activate your virtual environment using `workon` or `source`

Install package requirements using `pip`:

`pip install -r requirements.txt`

## Running Tests ##
Run tests using shell script `run`:

`./run`

You should see output from nose/unittest framework:
>..
>----------------------------------------------------------------------
> Ran 2 tests in 54.845s

Script will launch a set of tests for each browser (firefox & chrome) consecutively 

## What's included ? ##
### test_wikia.py ###
This file contains test scenarios as requested
### wikia_page_objects.py ###
This file contains page object classes

Since Python's implementation of Selenium Webdriver bindings doesn't have PageObject & PageFactory classes I had to implement those
as well as `find_by` helper function


~Valerie