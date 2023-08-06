import os
import pytest
from context import main
from main import *



#https://minimalmodbus.readthedocs.io/en/stable/develop.html#using-the-dummy-serial-port

def test_startup():
    assert lol() == "hi"