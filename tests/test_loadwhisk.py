from whisk.loadWhisk import loadWhiskerData
import os
import types
script_dir = os.path.dirname(__file__)
from pathlib import Path

def test_loadwhiskerdata():
    rel_path = 'testfiles'
    FILEPATH = os.path.join(script_dir, rel_path)
    whiskers = loadWhiskerData(Path(FILEPATH))

    assert(isinstance(whiskers,types.ModuleType))