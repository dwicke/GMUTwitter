import numpy as np
import math
from scipy.spatial import distance
from sklearn.cluster import DBSCAN #http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN.fit_predict
from sklearn import metrics
from collections import Counter

from twitterdata import TwitterData
from twitterdata import TwitterUser

userID = open('usrID.dat','r')
userPT = open('usrPT.dat','r')



points = []
skipIDxs = []
curSkipIDx = 0
numUsersWithLocal = 0
for line in userPT:
	x, y = line.split(u'\t', 1)
	fx = float(x)
	fy = float(y)
	if math.isnan(fx) == False or math.isnan(fy) == False:
		numUsersWithLocal += 1
		if math.fabs(fx - fy) > 0.06: # don't care about points that can't tell the difference between the top two locations
			points.append([float(x),float(y)])
			
		else:
			skipIDxs.append(curSkipIDx)
	else:
		skipIDxs.append(curSkipIDx)
	curSkipIDx += 1
	
userIDs = []
curSkipIDx = 0
for line in userID:
	if  curSkipIDx not in skipIDxs:
		userIDs.append(line.strip())
	curSkipIDx += 1

print len(userIDs)
print numUsersWithLocal

userID.close()
userPT.close()
##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.01, min_samples=10).fit(np.array(points)) # .01 and 5 is good with > .02
core_samples = db.core_sample_indices_
labels = db.labels_





import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

userF = open('localUserIDs2.dat','w')
userNF = open('nlocalUserIDs2.dat','w')


# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

i = 0
clust = [0] * n_clusters_
for pointD in points:
	if labels[i] == -1:
		pl.plot(pointD[0], pointD[1], 'o', markerfacecolor='k', markeredgecolor='k', markersize=4)
		userF.write(str(userIDs[i]) )
	else:
		pl.plot(pointD[0], pointD[1], 'o', markerfacecolor='b', markeredgecolor='b', markersize=4)
		userNF.write(str(userIDs[i]) )
		if clust[int(labels[i])] == 0:
			clust[int(labels[i])] = []
			clust[int(labels[i])].append(str(userIDs[i]))
		else:
			clust[int(labels[i])].append(str(userIDs[i]))
	i = i + 1	


	
userF.close()
userNF.close()


tweetData = TwitterData()
tweetData.twitterDataSetup('../training_set_users.txt', '../training_set_tweets.txt', 1000)
print 'printing stats'
tweetData.printStats()
print 'done'

locales = open('nlocals2.dat','w')
localesGen = open('locales2.dat', 'w')

iClust = 0
totsCount = Counter()
for curClust in clust:
	print 'Cur cluster' + str(iClust)
	countClus = Counter()
	for cluUID in curClust:
		#print str(tweetData.userIDDict[str(cluUID)].location)
		countClus.update([str(tweetData.userIDDict[str(cluUID)].location)])
		locales.write(str(iClust) + '\t' + str(tweetData.userIDDict[str(cluUID)].location) + '\t' + str(cluUID))
	totsCount.update(countClus)
	localesGen.write(str(countClus.most_common()) + '\n')
	iClust += 1
	
localesGen.write(str(totsCount.most_common())+'\n')

locales.close()
localesGen.close()
pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()


