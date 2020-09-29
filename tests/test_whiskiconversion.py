# PYTHON (just to be clear)
import matlab.engine
from pathlib import Path
import os

def test_conv_meas():
    """This test creates a numpy array and deletes it if the test passed. """
    eng = matlab.engine.start_matlab()
    filename = 'tests/testfiles/Ga_rc'
    print(eng.pwd())
    eng.addpath(eng.genpath('whiskiconversion'))
    eng.conv_meas_py(filename)
    eng.quit()

    my_testfile = Path("tests/testfiles/Ga_whiskermeasurements.npy")
    assert( my_testfile.is_file())
    if my_testfile.is_file():
        os.remove(my_testfile)


if __name__ == "__main__":
    test_conv_meas()
    print("Everything passed")