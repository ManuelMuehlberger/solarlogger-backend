import os
import pytest
from context import main
from main import *


def test_startup():
    assert lol() == "hi"