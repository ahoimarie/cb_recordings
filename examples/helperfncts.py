# helperfncts.py
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def position_fr_plot(sp, avgpos, isw_bin, whichbin, binwidth, bin1, xedges, whisking=True):
    """Plot average firing rates at each binned whisker position. """
    # for each cell
    acSize = int(np.ceil(np.sqrt(len(sp.stc))))
    avgFRinloc = []  # average firing rate in each discretized location

    left = 0.05  # the left side of the subplots of the figure
    right = 0.98  # the right side of the subplots of the figure
    bottom = 0.05  # the bottom of the subplots of the figure
    top = 0.9  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for space between subplots,
    # expressed as a fraction of the average axis width
    hspace = 0.2  # the amount of height reserved for space between subplots,
    # expressed as a fraction of the average axis height

    for cl in range(0, len(np.unique(sp.clu))):
        spikecountcluster = sp.stc[cl] # substitution
        if whisking:
            spikecountcluster = spikecountcluster[isw_bin]
        allFR = [spikecountcluster[whichbin == ic] / binwidth for ic in np.unique(whichbin)]  # all firing rates in each spatial bin
        allFRm = [np.mean(spikecountcluster[whichbin == ic] / binwidth) for ic in np.unique(whichbin)]  # mean of all firing rates
        avgFRinloc.append(allFR)

        plt.subplot(acSize, acSize, cl + 1)
        ax = sns.barplot(data=allFR[:-1], ci=68)
        # ax.set_xticklabels(np.round(xedges[:-1:2], 2))
        ax.set(xticks=range(0, bin1, 2))
        xrange = len(xedges) - 1
        scaling_meanFR = np.mean(allFRm)  # scale each subplot by mean firing rate of that cell
        plt.plot(scaling_meanFR * avgpos[:xrange], color='red')  # superimpose frequency of whisker in each position

        if cl == 0: ax.set(ylabel="FR (Hz)")
        if cl == len(np.unique(sp.clu)) - 1: ax.set(xlabel="zscored whisker position")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)

    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    # plt.show()
    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    # figManager.window.showMaximized() # different backend
    # plt.tight_layout()
    return ax


def whiskingpos(whiskdata, numBins, edges, whisker=0, rsam=15, whisking=True, locref="position", Fs =299):
    """Take the average of the whisker position over "rsam" samples. This effectively down-samples
    our whisker positions (to match our binned neural data) and should make it more robust
    against missing values (dropped frames).
    Whisker data (either position or whisking amplitude) are z-scored.
    If whisking=True, the average_position is only calculated during active whisking bouts. """

    if locref == 'position':
        whiskervar = stats.zscore(whiskdata.position[whisker])
    else:
        whiskervar = stats.zscore(whiskdata.amplitude[whisker])

    # reshape whisker variable over rsam samples (e.g. to average over rsam=15 samples)
    reshaped_whiskervar = np.reshape(whiskervar[:int(np.size(whiskervar) / rsam) * rsam], (-1, rsam)).T

    if not (len(reshaped_whiskervar.T) == numBins):
        print('Whisking and neural data mismatch length. ')
    # average position over whole recording
    average_position = np.mean(reshaped_whiskervar, axis=0)
    # if interested in position only during active whisking bouts:
    if whisking:
        flat_isw = [item / Fs for sublist in whiskdata.isw_sam[whisker] for item in sublist]
        samiisw, _ = np.histogram(flat_isw, bins=edges)
        isw_bin = list(map(bool, samiisw))  # Boolean iswhisking (yes/no) for each bin

        average_position = average_position[isw_bin]  # average position during active whisking
    else:
        isw_bin = []

    return average_position, isw_bin

