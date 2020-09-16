#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 2020

@author: Marie Tolkiehn

This script loads the whisking data and extracts the parts of the recording where whisking was detected.

It was previously shown that cerebellum linearly encodes whisker position during voluntary movement.
Chen, S., Augustine, G. J., & Chadderton, P. (2016). The cerebellum linearly encodes whisker position
during voluntary movement. ELife, 1–16. https://doi.org/10.7554/eLife.10509

Whisking parameter extraction is based on the script accompanies the Primer "Analysis of Neuronal Spike
Trains, Deconstructed", by J. Aljadeff, B.J. Lansdell, A.L. Fairhall and D. Kleinfeld (2016) Neuron,
91 link to manuscript: http://dx.doi.org/10.1016/j.neuron.2016.05.039

This script takes as input the filepath to the whisking data.
The input data consist of traces were generated by Nathan Clack's automated tracking of single rows of
whiskers in high-speed video Janelia https://wiki.janelia.org/wiki/display/MyersLab/Whisker+Tracking
The (huge) output files from the automated tracking were processed in Matlab using Janelia's available
code and converted to .npy using custom matlab function conv_meas_py.m available on github. The .npy
contain three columns [FID WhiskerLabels Angles], where FID corresponds to frame ID, whisker labels to
the whisker ID (0, 1, 2, ...) and the Angles to the measured angle of traced whiskers in degrees. Angles
are wrapped to 0-360 degrees. FIDs and Angles are linearly interpolated for missing frames. This
interpolation can be improved.

Please see https://github.com/ahoimarie/spikes-preprocessing for more explanation.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import glob
import sys

if os.path.join("../hilbert_transform") not in sys.path:
    sys.path.insert(0, "../hilbert_transform")


def loadWhiskerData(filepath):
    fileList = glob.glob(os.path.abspath(filepath) + '/*_whiskermeasurements.npy')
    import params as whiskdata

    whisk = np.load(Path(fileList[0]))

    df = pd.DataFrame(whisk, columns=['fid', 'labels', 'angles'])
    df = df.astype({'fid': int, 'labels': int})
    exptn = filepath.name[:-3]

    from hilbert_transforms import phase_from_hilbert
    from hilbert_transforms import get_slow_var

    # %% prepare whisking parameters
    fid = df['fid']
    angle = df['angles']
    label = df['labels']
    Fs = 299

    mid = exptn[0:6] + exptn[9]
    # nwhisk = len(np.unique(label))

    sr = Fs
    bp = [6, 30]  # lower and upper limits of band pass parameters of filter
    setpt_func = lambda x: (max(x) + min(x)) / 2.0  # function describing the setpoint location
    amp_func = np.ptp  # function describing the magnitude of amplitude
    thr = 10  # (degrees) threshold on whisker postion amplitude above which that part of a recording is taken to be a whisking bout
    a = 0.01  # 0.005 parameter for amplitude smoothing filter such that whisking bout 'cutouts' are not too short

    lag = 750  # % number of lags used to compute whisker autocorrelation
    tau = [x / sr for x in range(-lag, lag, 1)]  # % autocorrelation temporal lag vector

    # Interpolated values
    angles = angle  # % or 'angle'
    fids = fid  # ;% or fid
    labels = label  # ; % or label

    # maximum number of frames
    nsamp = max(fid)

    # for i = 1
    from scipy.signal import filtfilt, butter

    if -1 in labels:
        nrec = len(np.unique(labels)) - 1
    else:
        nrec = len(np.unique(labels))
    k = 0

    # for each whisking bout recorded we will have a cell array that contains
    # the following variables
    isw_isam = []  # sample numbers
    iisw_ispk = []  # sample numbers during which a spike was recorded
    isw_itop = []  # sample numbers during the whisker position has a peak
    isw_pos = []  # whisker position
    isw_phs = []  # whisker phase
    isw_amp = []  # whisker amplitude
    isw_spt = []  # whisker set-point
    isw_sam = []  # sample id

    # arrays that will hold relevant information for each recording interval:
    samp = []
    time = []
    phase = []
    amplitude = []
    spikes = []
    setpoint = []
    position = []
    tops = []
    iswhisking = []  # a list of indices pointing to times where the animal was whisking

    ACisw = np.zeros((2 * lag + 1, 100))  # % autocorrelation of whisker position during whisking
    ACall = np.zeros((2 * lag + 1, nrec))  # % autocorrelation of whisker position during all times

    for j in np.unique(labels):
        pos = np.array(np.transpose(angles[labels == j]))  # % angle during recording
        sam = np.array(np.transpose(fids[labels == j])) - 1  # % sample number
        # spk = np.array(np.transpose(sp.st[sp.clu==sp.clu[i]]))  #% samples during which spike was recorded

        phs, _ = phase_from_hilbert(pos, sr, bp)  # % extracting phase from whisker position using hilbert transform

        amp, itop, ibot = get_slow_var(pos, phs, amp_func)
        spt, _, _ = get_slow_var(pos, phs, setpt_func)

        [bb, aa] = butter(1, a / 3)
        # ACall[:,j] = np.correlate(amp*cos(phs)/2,lag,'full') # needs work
        # ampfilt = filtfilt(a,[1,a-1],amp,padtype = 'odd',
        # padlen=3*(max(np.size(a),len([1,a-1]))-1)) # almost identical to Aljadeffs ver
        ampfilt = filtfilt(bb, aa, amp, padtype='odd', padlen=3 * (max(np.size(bb), len(aa)) - 1))

        iisw = np.heaviside(ampfilt - thr, .5)  # % indices of times where the animal was whisking
        iisam = sam[iisw == True]
        isw_con = group_consecutives(iisam, step=1)  # connected components of whisking for each whisking bout
        ic = 0
        tisw_isam = []  # sample numbers
        tiisw_ispk = []  # sample numbers during which a spike was recorded
        tisw_itop = []  # sample numbers during the whisker position has a peak
        tisw_pos = []  # whisker position
        tisw_phs = []  # whisker phase
        tisw_amp = []  # whisker amplitude
        tisw_spt = []  # whisker set-point
        tisw_sam = []  # sample id
        for iisw_temp in isw_con:
            #  looping over connected components of the vector iisw1 (each connected component is a whisking bout)
            #  the variables in each whisking bout (indexed by k) are put into the appropriate cell array
            k += 1
            tisw_isam.append(iisw_temp)
            tisw_itop.append(np.intersect1d(itop, iisw_temp))
            tisw_pos.append(pos[iisw_temp])
            tisw_phs.append(phs[iisw_temp])
            tisw_amp.append(amp[iisw_temp])
            tisw_spt.append(spt[iisw_temp])
            tisw_sam.append(sam[iisw_temp])

            ic += 1

        isw_isam.append(tisw_isam)
        isw_itop.append(tisw_itop)
        isw_pos.append(tisw_pos)
        isw_phs.append(tisw_phs)
        isw_amp.append(tisw_amp)
        isw_spt.append(tisw_spt)
        isw_sam.append(tisw_sam)

        samp.append(sam)
        phase.append(phs)
        amplitude.append(amp)
        # spikes.append(spk)
        tops.append(itop)
        setpoint.append(spt)
        position.append(pos)
        iswhisking.append(iisw)
        # mic.append(len(isw_con))
        time.append(np.arange(0, max(sam) + 1) / float(sr))

    # %% Loading whiskers as eventTimes

    eventTimes = []
    [eventTimes.append([item[0] / sr for item in isw_sam[j]]) for j in range(len(isw_sam))]
    # breakpoint()
    whiskdata.df = df  # FID, labels, angles
    whiskdata.mid = mid  # mouse ID
    whiskdata.samp = samp
    whiskdata.time = time
    whiskdata.phase = phase
    whiskdata.amplitude = amplitude
    whiskdata.spikes = spikes
    whiskdata.setpoint = setpoint
    whiskdata.position = position
    whiskdata.tops = tops
    whiskdata.iswhisking = iswhisking
    whiskdata.isw_isam = isw_isam
    whiskdata.isw_itop = isw_itop
    whiskdata.isw_pos = isw_pos
    whiskdata.isw_phs = isw_phs
    whiskdata.isw_amp = isw_amp
    whiskdata.isw_spt = isw_spt
    whiskdata.isw_sam = isw_sam
    whiskdata.eventTimes = eventTimes

    return whiskdata


def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        exit("Too few arguments calling script")

    exptn = sys.argv[1]
