# Artiom Dolghi

import numpy as np
from matplotlib import pyplot as plt

arr = np.load("pop2010.npy")

lorenzSum = arr.cumsum() / arr.sum()
lorenzCurve = np.insert(lorenzSum, 0, 0)

plt.plot(np.linspace(0.0, 1.0, lorenzCurve.size), lorenzCurve)
plt.plot([0,1], [0,1])

plt.title("Lorenz Curve of Various Country Populations")
plt.xlabel("Cumulative Country Size")
plt.ylabel("Cumulative Contribution to Common Population")

plt.savefig("population-lorenz.png", dpi = 200)
