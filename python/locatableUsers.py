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
	
userID.close()
userPT.close()

locales = open('finalLocals.dat','w')
for uID in userIDs:
	locales.write(str(uID) + '\n')
	
locales.close()
