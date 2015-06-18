### IMPORTS ###
import pandas as pd
import numpy as np
import json
from pprint import pprint
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter
import time
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import Birch
from matplotlib.mlab import PCA as mlabPCA

# reading in data
with open('/users/trevorsmith/Desktop/fda_topic_modeling/warning_labels_lda_15_dict.json') as data_file:
    data = json.load(data_file)

# we now have a dictionary
# but each key has a value that is a list
# need to convert this list into another dictionary
data_test = {}
data_sub_test = {}

for key, value in data.items():
    data_sub_test = {}
    for i in value:
#         print str(i[0]) + "~" + str(i[1])
        data_sub_test[i[0]] = i[1]
        data_test[key] = data_sub_test

# now our data is formatted correctly, let's read into a DF
df = pd.DataFrame.from_dict(data_test, orient='index')

# let's take a look at our data
print df.head()

# we now have our 25 columns...each representing a topic.  SUCCESS!
# now we need to fill na's with 0's
df.fillna(0, inplace=True)

### CLUSTERING ###

# let's convert to numpy array for faster processing
all_samples = df.as_matrix()

# let's work with a subset first so we don't crash anything :)
small_sample = all_samples[:10000]

# ok, now let's loop through and find the optimal num of clusters
start_time = time.time()
max_clusters = 20
inertia_curve = []
colors = []
colours = []

for num in range (max_clusters):
    # color = np.random.rand(3,)
    # colours.append(color)
    # colors = list(colours)

for cluster in range(max_clusters)[2:]:
    num_clusters = cluster
    km = MiniBatchKMeans(init='k-means++', n_clusters=num_clusters)
    km.fit_predict(small_sample)
    clusters = km.labels_.tolist()
    inertia = km.inertia_
    inertia_curve.append(round(inertia,4))
    cluster_range = range(cluster)[1:]
    labels = km.labels_
    print "Silhouette score:", metrics.silhouette_score(df, labels, metric='euclidean')
    print "Number of clusters:", cluster
    print Counter(clusters)

    # now convert to array for plotting
plt.plot(cluster_range, inertia_curve, label = 'Inertia Curve')
plt.legend()
plt.show()


