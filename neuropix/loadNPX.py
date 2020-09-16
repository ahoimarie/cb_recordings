# from __init__ import *
# from neuropix.loadNeuropix import loadKsDir # was *
#
# myKsDir = FILEPATH
#
# # myEventTimes = load('C:\...\data\someEventTimes.mat'); # a vector of times in seconds of some event to align to
#
# if full_path not in sys.path:
#     # sys.path.insert(1, full_path)
#     sys.path.append(full_path)
#
#
# #%% Loading data from kilosort/phy easily
# sp = loadKsDir(myKsDir)
#
# # sp.st are spike times in seconds
# # sp.clu are cluster identities
# # spikes from clusters labeled "noise" have already been omitted
# sp.st = sp.st-1  # recording started 1s before video (SpikeGLX feature) # XXX
# sp.spikeTemplates = sp.spikeTemplates[sp.st > 0]
# sp.clu = sp.clu[sp.st > 0]
# sp.tempScalingAmps[sp.st > 0]
# sp.st = sp.st[sp.st > 0]
#
# sortedDepth = np.sort(sp.depth)
# sortid = np.argsort(sp.depth)
# sp.cidsSorted = sp.cids.iloc[sortid].reset_index(drop=True)  # sorted cids from deepest to most superficial cluster
# sp.sortedDepth = sortedDepth
