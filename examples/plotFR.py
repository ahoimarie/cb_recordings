#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import seaborn as sns
import numpy as np
from math import log2
from initparams import *
from whiskers.loadWhisk import loadWhiskerData
from neuropix.loadNeuropix import loadKsDir, process_spiketimes
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
sns.set(color_codes=True)
plt.rcParams.update({'font.size': 10})
from examples.helperfncts import position_fr_plot,whiskingpos

#------------------------------------------------------------------------------
# Load and process
#------------------------------------------------------------------------------
whiskd = loadWhiskerData(FILEPATH)
sp = loadKsDir(FILEPATH)
sp = process_spiketimes(sp)

locref = "position"
whisking = False
Fs = 299  # samples/s, video sampling rate Fs = 299
# binwidth = 0.1003; % 100.3 ms
rsam = 15  # number of samples
binwidth = rsam / Fs  # 50 ms % average over 15 samples
nsamp = max([i[-1] for i in whiskd.samp])
# binarise spike times
edges = np.arange(0, nsamp / Fs, binwidth)

# Create spike count in non-overlapping individual time bins
sp.stc = []
for cl in range(0, len(np.unique(sp.clu))):
    nb, edg = np.histogram(sp.st[sp.clu == sp.cidsSorted[cl]], bins=edges)  # sorted by depth
    sp.stc.append(nb)  # % spike count

# nb should be the size len(whiskervar[:int(np.size(whiskervar)/rsam)*rsam])/rsam

nwhisk = np.size(np.unique(whiskd.df.labels))  # number of whiskers

# %% creating histograms of mean firing rate per bin at different positions
#------------------------------------------------------------------------------
# Calculate average position and average firing rate for each cell
#------------------------------------------------------------------------------

for whisker in range(1, 2):  # range(nwhisk):

    average_position, isw_bin = whiskingpos(whiskd, len(nb),edges, whisker, rsam, whisking)
    # binsizes
    # getting the optimal number of bins
    bin1 = round(1 + log2(np.size(average_position)))
    xedges = np.linspace(min(average_position), max(average_position), bin1 + 1)

    # calculate histogram over spatial position to get frequency of each location
    [pos, edg] = np.histogram(average_position, xedges, density=True)
    whichbin = np.digitize(average_position, xedges)

    plt.close('all')
    position_fr_plot(sp, pos, isw_bin, whichbin, whisking)

    fname = "Mean firing rate vs " + locref + ", " + whiskd.mid + ", wh" + str(whisker) + ", bin " + str(
        round(binwidth * 1000, 2)) + "ms, whisking " + str(whisking) + ", depthsorted"

    plt.suptitle(fname)

    figname = figpath + '/' + fname + ".png"
    if Path(figname).exists():
        print("Filename already exists, did not save.")
    else:
        plt.savefig(figpath + '/' + fname + ".png")

print("Done")


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        exit("Too few arguments calling script")

    EXPTN = sys.argv[1]

