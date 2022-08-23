import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kde
from scipy.stats import pearsonr
import pandas as pd
from scipy.stats import rankdata

matrix_5hmc = pd.read_csv('./tmp_data/lung_cancer/lung_matrix.5hmc.bed', sep='\t')
matrix_5mc = pd.read_csv('./tmp_data/lung_cancer/lung_matrix.5mc.bed', sep='\t')

m5mc = matrix_5mc.iloc[:, 3:]
m5hmc = matrix_5hmc.iloc[:, 3:]

a = (m5mc == -1).sum(1) == 0
b = (m5hmc == -1).sum(1) == 0
mc = m5mc[a * b].mean(1)
hmc = m5hmc[a * b].mean(1)

x = mc.to_numpy()[1:10000]
y = hmc.to_numpy()[1:10000]

x = rankdata(x)
y = rankdata(y)
nbins = 300
k = kde.gaussian_kde([x, y])
xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto')
plt.colorbar()
plt.show()

print(pearsonr(x, y))

