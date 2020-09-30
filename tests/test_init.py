from initparams import *
import os
from setup import _package_tree

def test_always_passes():
    assert (figpath == "figs")

def test_setup():
    script_dir = os.path.dirname(__file__)
    rel_path = '../setup.py'
    FILEPATH = os.path.join(script_dir, rel_path)
    assert(Path(FILEPATH).exists() )

def test_setupdef():
    _package_tree()