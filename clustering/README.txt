cluster.py - hierachical K-means

Runs until cluster assignments do not change. Modify the distance 
method to implement other distance functions. Currently the file
takes a single argument, which is a file that is space separated
where each row is a point.

Outputs a file cluster.json which contains the centroids and the 
labels for that node in the hierarchy.

classify.py - classification using cluster.json

Uses centriods that were saved off to search for labels of data.
Outputs a list of likely cities for each data vector as well
as the known label for that data (for testing). It will create 
2 files results.txt which contains the results of the labeling 
per data point and stats.txt which contains overall stats
on how successful the labeling was.
