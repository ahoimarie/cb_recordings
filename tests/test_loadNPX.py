import pytest
import numpy as np
from .neuropix.loadNeuropix import loadKsDir
# from neuropix.loadNeuropix import process_spiketimes
# from whisk.loadWhisk import loadWhiskerData
import os
import types
script_dir = os.path.dirname(__file__)

def test_loadKsdir():
    rel_path = 'testfiles'
    FILEPATH = os.path.join(script_dir, rel_path)
    print(FILEPATH)
    spikes = loadKsDir(FILEPATH)
    assert(isinstance(spikes,types.ModuleType))


#
# def test_get_slow_var():
#     amp_func = np.ptp #peak to peak
#     sr = 299
#     bp = [6,30]
#     x = np.arange(0, 10, 0.1)
#     pos = np.sin(x)
#     phs,_ = phase_from_hilbert(pos,sr,bp)
#     testamp = np.ndarray.flatten(np.load(os.path.join(os.path.dirname(__file__),'hilbamptest.npy')))
#
#     amp,itop,ibot = get_slow_var(pos,phs,amp_func)
#
#     np.testing.assert_allclose(testamp[0:30], amp[0:30], rtol=0.1)




if __name__ == "__main__":
    test_loadKsdir()
    # test_get_slow_var()
    print("Everything passed")