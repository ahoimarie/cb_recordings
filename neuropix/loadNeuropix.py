#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 2020

@author: Marie Tolkiehn
"""

import numpy as np
import pandas as pd

from pathlib import Path
import os.path


# %%

def loadKsDir(ksdir, *args):
    varargin = args
    if varargin:
        params = varargin;
    else:
        # params = [];
        params = type('', (), {})()

    if not hasattr(params, 'excludeNoise'):  # ~isfield(params, 'excludeNoise'):
        params.excludeNoise = True

    if not hasattr(params, 'loadPCs'):  # ~isfield(params, 'loadPCs'):
        params.loadPCs = False

    import sys
    full_path = os.path.join(ksdir)
    if full_path not in sys.path:
        sys.path.append(full_path)


    # import importlib.util
    # spec = importlib.util.spec_from_file_location("params", module_path)
    # foo = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(foo)

    import params as spikeStruct

    # breakpoint()
    ss = np.load(Path(full_path, "spike_times.npy"))
    # ss = np.load("spike_times.npy")

    st = np.double(ss) / spikeStruct.sample_rate
    spikeTemplates = np.load(Path(full_path, "spike_templates.npy"))
    if Path(full_path, "spike_clusters.npy").exists():
        clu = np.load(Path(full_path, "spike_clusters.npy"))
    else:
        clu = spikeTemplates

    tempScalingAmps = np.load(Path(full_path, "amplitudes.npy"))
    if params.loadPCs:
        pcFeat = np.load(Path(full_path, 'pc_features.npy'));  # % nSpikes x nFeatures x nLocalChannels
        pcFeatInd = np.load(Path(full_path, 'pc_feature_ind.npy'));  # % nTemplates x nLocalChannels
    else:
        pcFeat = [];
        pcFeatInd = [];

    cgsFileref = ''
    if Path(full_path, "cluster_groups.csv").exists():
        cgsFileref = Path(full_path, "cluster_groups.csv")
    if Path(full_path, "cluster_group.tsv").exists():
        cgsFileref = Path(full_path, "cluster_group.tsv")
    if Path(full_path, "cluster_info.tsv").exists():
        cinfo = Path(full_path, "cluster_info.tsv")

    if cgsFileref:
        clinfo = pd.read_csv(cinfo, delimiter='\t')
        clinfo.group.fillna('unsorted', inplace=True)
        clinfo['cgs'] = clinfo.group.map({'noise': 0, 'mua': 1, 'good': 2, 'unsorted': 3})

        if params.excludeNoise:
            noiseclusters = clinfo.id[clinfo.cgs == 0]
            # np.in1d(array1, array2)
            st = st[np.in1d(clu, noiseclusters, invert=True)]  # remove noise clusters
            spikeTemplates = spikeTemplates[np.in1d(clu, noiseclusters, invert=True)]
            tempScalingAmps = tempScalingAmps[np.in1d(clu, noiseclusters, invert=True)]

            depth = clinfo.depth[np.in1d(clinfo.id, noiseclusters, invert=True)]
            clu = clu[np.in1d(clu, noiseclusters, invert=True)]
            cgs = clinfo.cgs[np.in1d(clinfo.id, noiseclusters, invert=True)]
            cids = clinfo.id[np.in1d(clinfo.id, noiseclusters, invert=True)]

    coords = np.load(Path(full_path, "channel_positions.npy"))
    ycoords = coords[:, 1];
    xcoords = coords[:, 0];

    temps = np.load(Path(full_path, "templates.npy"))
    winv = np.load(Path(full_path, "whitening_mat_inv.npy"))

    spikeStruct.st = st.flatten();
    spikeStruct.spikeTemplates = spikeTemplates;
    spikeStruct.clu = clu;
    spikeStruct.tempScalingAmps = tempScalingAmps;
    spikeStruct.cgs = cgs;
    spikeStruct.cids = cids;
    spikeStruct.depth = depth;  # % added by Marie Tolkiehn
    spikeStruct.xcoords = xcoords;
    spikeStruct.ycoords = ycoords;
    spikeStruct.temps = temps;
    spikeStruct.winv = winv;
    spikeStruct.pcFeat = pcFeat;
    spikeStruct.pcFeatInd = pcFeatInd;

    return spikeStruct