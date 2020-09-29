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
# Definitions
#------------------------------------------------------------------------------

# def position_fr_plot(sp, avgpos, isw_bin, whichbin, whisking=True):
#     """Plot average firing rates at each binned whisker position. """
#     # for each cell
#     acSize = int(np.ceil(np.sqrt(len(sp.stc))))
#     avgFRinloc = []  # average firing rate in each discretized location
#
#     left = 0.05  # the left side of the subplots of the figure
#     right = 0.98  # the right side of the subplots of the figure
#     bottom = 0.05  # the bottom of the subplots of the figure
#     top = 0.9  # the top of the subplots of the figure
#     wspace = 0.2  # the amount of width reserved for space between subplots,
#     # expressed as a fraction of the average axis width
#     hspace = 0.2  # the amount of height reserved for space between subplots,
#     # expressed as a fraction of the average axis height
#
#     for cl in range(0, len(np.unique(sp.clu))):
#         spikecountcluster = sp.stc[cl] # substitution
#         if whisking:
#             spikecountcluster = spikecountcluster[isw_bin]
#         allFR = [spikecountcluster[whichbin == ic] / binwidth for ic in np.unique(whichbin)]  # all firing rates in each spatial bin
#         allFRm = [np.mean(spikecountcluster[whichbin == ic] / binwidth) for ic in np.unique(whichbin)]  # mean of all firing rates
#         avgFRinloc.append(allFR)
#
#         plt.subplot(acSize, acSize, cl + 1)
#         ax = sns.barplot(data=allFR[:-1], ci=68)
#         # ax.set_xticklabels(np.round(xedges[:-1:2], 2))
#         ax.set(xticks=range(0, bin1, 2))
#         xrange = len(xedges) - 1
#         scaling_meanFR = np.mean(allFRm)  # scale each subplot by mean firing rate of that cell
#         plt.plot(scaling_meanFR * avgpos[:xrange], color='red')  # superimpose frequency of whisker in each position
#
#         if cl == 0: ax.set(ylabel="FR (Hz)")
#         if cl == len(np.unique(sp.clu)) - 1: ax.set(xlabel="zscored whisker position")
#         ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)
#
#     plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
#     # plt.show()
#     figManager = plt.get_current_fig_manager()
#     figManager.resize(*figManager.window.maxsize())
#     # figManager.window.showMaximized() # different backend
#     # plt.tight_layout()
#     return ax
#
#
# def whiskingpos(whiskdata, numBins, whisker=0, rsam=15, whisking=True, locref="position"):
#     """Take the average of the whisker position over "rsam" samples. This effectively down-samples
#     our whisker positions (to match our binned neural data) and should make it more robust
#     against missing values (dropped frames).
#     Whisker data (either position or whisking amplitude) are z-scored.
#     If whisking=True, the average_position is only calculated during active whisking bouts. """
#
#     if locref == 'position':
#         whiskervar = stats.zscore(whiskdata.position[whisker])
#     else:
#         whiskervar = stats.zscore(whiskdata.amplitude[whisker])
#
#     # reshape whisker variable over rsam samples (e.g. to average over rsam=15 samples)
#     reshaped_whiskervar = np.reshape(whiskervar[:int(np.size(whiskervar) / rsam) * rsam], (-1, rsam)).T
#
#     if not (len(reshaped_whiskervar.T) == len(numBins)):
#         print('Whisking and neural data mismatch length. ')
#
#     # average position over whole recording
#     average_position = np.mean(reshaped_whiskervar, axis=0)
#     # if interested in position only during active whisking bouts:
#     if whisking:
#         flat_isw = [item / Fs for sublist in whiskdata.isw_sam[whisker] for item in sublist]
#         samiisw, _ = np.histogram(flat_isw, bins=edges)
#         isw_bin = list(map(bool, samiisw))  # Boolean iswhisking (yes/no) for each bin
#
#         average_position = average_position[isw_bin]  # average position during active whisking
#     else:
#         isw_bin = []
#
#     return average_position, isw_bin
#

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

