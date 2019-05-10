from trajminer.similarity import LCSS, EDR, pairwise_similarity
from trajminer.clustering import DBSCAN
from trajminer.utils import CSVTrajectoryLoader
from trajminer.utils.distance import discrete, euclidean, haversine
import numpy as np

import datetime

timeBegining = datetime.datetime.now()
print(timeBegining)
loader = CSVTrajectoryLoader('test-500taxi-cluster.csv', label_col=None, tid_col='tid', lat='lat', lon='long', n_jobs=15)
dataset = loader.load()
print(dataset.get_attributes())

dist_functions = [euclidean]
thresholds = [100]
lcss = LCSS(dist_functions, thresholds)

distanceMatrixVar = pairwise_similarity(dataset.get_trajectories(), measure = lcss,n_jobs= 100)
distanceMatSave = np.array(distanceMatrixVar)
np.savetxt('distMatrix.txt',distanceMatSave, fmt='%1.3f')
# Do something with the generated clusters
print(distanceMatrixVar)
timeEnd = datetime.datetime.now()
print("Time of end was: ")
print(timeEnd)
print(timeEnd - timeBegining)
