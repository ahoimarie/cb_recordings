from neuropix.loadNeuropix import loadKsDir
import os
import types
script_dir = os.path.dirname(__file__)
from pathlib import Path


def test_loadKsdir():
    rel_path = 'testfiles'
    FILEPATH = os.path.join(script_dir, rel_path)
    print(FILEPATH)
    spikes = loadKsDir(Path(FILEPATH))
    assert(isinstance(spikes,types.ModuleType))


if __name__ == "__main__":
    test_loadKsdir()
    # test_get_slow_var()
    print("Everything passed")