# %% histogram stuff histogram
import seaborn as sns
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import stats
from math import log2
from setup import *
from whisk.LoadWhisk import loadWhiskerData
from neuropix.loadNPX import *
sns.set(color_codes=True)

whiskd = loadWhiskerData(filepath)

Fs = 299  # samples/s
# binwidth = 0.1003; % 100.3 ms
rsam = 15  # number of samples
binwidth = rsam / Fs  # 50 ms % average over 15 samples

# nsamp = max(isam);
nsamp = max([i[-1] for i in whiskd.samp])
# video sampling rate Fs = 299
# binarise spike times
edges = np.arange(0, nsamp / Fs, binwidth)

# Create spike count in individual time bins
sp.stc = []
for cl in range(0, len(np.unique(sp.clu))):
    nb, edg = np.histogram(sp.st[sp.clu == sp.cidsSorted[cl]], bins=edges)  # %sorted by depth
    sp.stc.append(nb)  # % spike count

nwhisk = np.size(np.unique(whiskd.df.labels))

# %% creating histograms of mean firing rate per bin at different positions
whisking = True
for whisker in range(1):# range(nwhisk):
    # whisker = 0
    locref = 'position'

    if locref == 'position':
        A = stats.zscore(whiskd.position[whisker])
    else:
        A = stats.zscore(whiskd.amplitude[whisker])

    out = np.reshape(A[:int(np.size(A) / rsam) * rsam], (-1, rsam)).T

    if not (len(out.T) == len(nb)):
        print('Whisking and neural data mismatch length. ')

    average_position = np.mean(out, axis=0)
    if whisking:
        flat_isw = [item / Fs for sublist in whiskd.isw_sam[whisker] for item in sublist]
        samiisw, _ = np.histogram(flat_isw, bins=edges)
        isw_bin = list(map(bool, samiisw))

        # isw_bin = whiskd.iswhisking[whisker]#[i for i in range(len(average_position)) if i in flat_isw]
        average_position = average_position[isw_bin]

    # binsizes
    # getting the optimal number of bins
    bin1 = round(1 + log2(np.size(average_position)))
    xedges = np.linspace(min(average_position), max(average_position), bin1 + 1)
    # calculate histogram over spatial position
    [n, edg] = np.histogram(average_position, xedges, density=True)
    whichbin = np.digitize(average_position, xedges)

    # % for each cell
    acSize = int(np.ceil(np.sqrt(len(sp.stc))))
    avgFRinloc = []

    plt.close('all')

    left = 0.125  # the left side of the subplots of the figure
    right = 0.9  # the right side of the subplots of the figure
    bottom = 0.1  # the bottom of the subplots of the figure
    top = 0.9  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for space between subplots,
    # expressed as a fraction of the average axis width
    hspace = 0.2  # the amount of height reserved for space between subplots,
    # expressed as a fraction of the average axis height

    for cl in range(0, len(np.unique(sp.clu))):
        # b = sp.stc[cl][:len(average_position)]
        b = sp.stc[cl]
        if whisking:
            b = b[isw_bin]
        allFR = [b[whichbin == ic] / binwidth for ic in np.unique(whichbin)]
        allFRm = [np.mean(b[whichbin == ic] / binwidth) for ic in np.unique(whichbin)]

        # allFRd[cl] = allFR

        avgFRinloc.append(allFR)

        plt.subplot(acSize, acSize, cl + 1)
        #    plt.bar(xedges[:-1], allFRm[:-1])
        # sns.barplot(xedges[:-1], allFR[:-1])
        # dfFR = pd.DataFrame(dict(x=xedges, y=allFR))
        # ax = sns.barplot(x="x", y="y", data=dfFR, ci=68)
        ax = sns.barplot(data=allFR[:-1], ci=68)
        # ax.set_xticklabels(np.round(xedges[:-1:2], 2))
        ax.set(xticks=range(0, bin1, 2))
        xrange = len(xedges) - 1
        scaling_meanFR = np.mean(allFRm)
        plt.plot(scaling_meanFR * n[:xrange], color='red')

        if cl == 0: ax.set(ylabel="FR (Hz)")
        if cl == len(np.unique(sp.clu)) - 1: ax.set(xlabel="zscored position")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)

    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    # plt.show()
    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    # figManager.window.showMaximized()
    # plt.tight_layout()

    fname = "Mean firing rate vs " + locref + ", " + whiskd.mid + ", wh" + str(whisker) + ", bin " + str(
        round(binwidth * 1000, 2)) + "ms, whisking " + str(whisking) + ", depthsorted"

    plt.suptitle(fname)

    figname = figpath + '/' + fname + ".png"
    if Path(figname).exists():
        print("Filename already exists, did not save.")
    else:
        plt.savefig(figpath + '/' + fname + ".png")


