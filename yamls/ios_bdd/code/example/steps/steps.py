from behave import *
import sys
import os
home = os.getenv('HOME')
main_path = home + '/sisyphus/boulder'
sys.path.insert(0, main_path)
from pebble import pebble
import allure

@given("")
def step(self):
    assert pebble.push(('example', 1))
