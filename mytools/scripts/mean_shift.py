import numpy as np
import sys
from sklearn.cluster import MeanShift, estimate_bandwidth

def read_nums(file_int):
    with open(file_int) as infile:
        nums = []
        for line in infile:
            line = line.strip()
            try:
                nums.append(int(line))
            except ValueError:
                continue
    nums.sort()
    return nums

x = read_nums(sys.argv[1])

X = np.array(zip(x,np.zeros(len(x))), dtype=np.int)
bandwidth = estimate_bandwidth(X, quantile=float(sys.argv[2]))
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print "\t".join(['num','pos'])
for k in range(n_clusters_):
    my_members = labels == k
    for num in X[my_members, 0]:
        print "\t".join([str(i) for i in [k, num]])