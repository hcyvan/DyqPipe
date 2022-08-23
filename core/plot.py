import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from scipy.stats import pearsonr
from scipy.stats import rankdata


def plot_cor_heatmap(x, y, sample=20000, output="test.png", xlabel='X', ylabel='Y'):
    if len(x) > sample:
        choice_idx = np.random.choice(range(len(x)), 20000)
        x = x[choice_idx]
        y = y[choice_idx]
    x = rankdata(x)
    y = rankdata(y)
    cor = pearsonr(x, y)
    nbins = 300
    k = gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    # https://www.python-graph-gallery.com/85-density-plot-with-matplotlib
    # https://matplotlib.org/stable/gallery/color/colormap_reference.html
    # plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto',cmap=plt.cm.jet)
    parameters = {
        'axes.labelsize': 15,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'axes.titlesize': 15
    }
    plt.rcParams.update(parameters)

    plt.figure(figsize=(5, 4), dpi=300)
    plt.title('R: {r}, P-value: {p}'.format(r=round(cor.statistic, 2), p=cor.pvalue))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto')
    plt.tight_layout()
    plt.colorbar()
    plt.savefig(output)
    # plt.show()
