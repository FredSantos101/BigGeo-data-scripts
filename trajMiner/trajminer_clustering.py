from trajminer.similarity import LCSS, EDR
from trajminer.clustering import DBSCAN
from trajminer.utils import CSVTrajectoryLoader
from trajminer.utils.distance import discrete, euclidean, haversine

import datetime

timeBegining = datetime.datetime.now()
print(timeBegining)
loader = CSVTrajectoryLoader('test-500taxi-cluster.csv', label_col=None, tid_col='tid', lat='lat', lon='lon', n_jobs=15)
dataset = loader.load()
print(dataset.get_attributes())

loader = CSVTrajectoryLoader('test-500taxi-cluster-label.csv', label_col=None, tid_col='tid', lat='lat', lon='lon', n_jobs=15)
dataset2 = loader.load()
print(dataset.get_attributes())

# Distance functions and thresholds for each attribute.
# i-th distance function/threshold corresponds to the i-th attribute
dist_functions = [euclidean]
thresholds = [50]
edr = EDR(dist_functions, thresholds)

clustering = DBSCAN(eps=0.1, min_samples=2, measure='preprocessed', n_jobs=15)

pred_labels = clustering.fit_predict(dataset.get_trajectories())
true_labels = dataset.get_labels()
print(pred_labels)
# Do something with the generated clusters

timeEnd = datetime.datetime.now()
print("Time of end was: ")
print(timeEnd)
print(timeEnd - timeBegining)
