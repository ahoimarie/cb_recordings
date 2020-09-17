# from neuropix.loadNeuropix import loadKsDir
from examples.helperfncts import whiskingpos
from whisk.loadWhisk import loadWhiskerData
import os
import numpy as np
# import types
script_dir = os.path.dirname(__file__)
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def get_whiskerdata():
    rel_path = './testfiles'
    FILEPATH = os.path.join(script_dir, rel_path)
    whiskerdata = loadWhiskerData(Path(FILEPATH))
    return whiskerdata


@pytest.mark.parametrize('whisking, avglen, lenisw', [
    (False, 25507, 0),
    (True, 11672, 25507),
    (None, 25507, 0),
])
def test_whiskingposFX(get_whiskerdata, whisking, avglen, lenisw):
    Fs = 299  # samples/s, video sampling rate Fs = 299
    # binwidth = 0.1003; % 100.3 ms
    rsam = 15  # number of samples
    nsamp = max([i[-1] for i in get_whiskerdata.samp])
    edges = np.arange(0, nsamp / Fs, rsam/Fs)
    numBins = int( len(get_whiskerdata.position[0][:int(np.size(get_whiskerdata.position[0]) / rsam) * rsam]) / int(rsam) )

    average_position, isw_bin = whiskingpos(get_whiskerdata, numBins, edges, 0, rsam, whisking)
    assert ((len(average_position) == avglen) & (len(isw_bin) == lenisw))


def test_always_passes():
    assert True

# def test_always_fails():
#     assert False

if __name__ == "__main__":
    # test_whiskingpos()
    test_whiskingposFX()
    print("Everything passed")
