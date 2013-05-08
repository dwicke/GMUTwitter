
#http://dns2.icar.cnr.it/manco/Teaching/2005/datamining/articoli/KDD-96.final.frame.pdf
from collections import Counter
from twitterdata import TwitterData
from twitterdata import TwitterUser
import re
import codecs
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import DBSCAN #http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN.fit_predict
from sklearn import metrics

## word\tprobability 
f = codecs.open('fetr.dat', u'r', u'utf-8')
localDict = {}

for line in f:
	word, ratio, prob = line.split(u'\t', 2)
	if float(prob) > 0.5: ## only use words that have a > %50 chance of being local
		localDict[word] = float(prob)
	
print len(localDict)

f.close()


def my_tokenizer(s):
	tokens = []
	for tok in s.split():
		if tok in localDict:
			tokens.append(tok)
	return tokens


tweetData = TwitterData()
tweetData.twitterDataSetup('../training_set_users.txt', '../training_set_tweets.txt', 1000)
print 'printing stats'
tweetData.printStats()
print 'done'

bgwords = [] ## maps userID to the start index in points data

print len(tweetData.userIDDict)
points = []
listLocal = list(localDict)
usrNumLoc = []
for usrID, usr in tweetData.userIDDict.items():
	allTweets = " ".join(usr.tweets) # join all of the user's tweets
	tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
	c = Counter(tokenized) # make the bag of words for the user any word not in the dict means not present
	if len(list(c)) > 0:
		
		holdLen = len(points)
		for word in list(c):
			weight = c[word] * localDict[word]
			if weight > 2:
				points.append([listLocal.index(word), weight])
		if holdLen != len(points):
			bgwords.append([usrID, len(points)])
			
points = np.array(points) ## needs to be a numpy array to work


print len(bgwords)

##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=5).fit(points)
core_samples = db.core_sample_indices_
labels = db.labels_





import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

userF = open('localUserIDs.dat','w')
userNF = open('nlocalUserIDs.dat','w')
i = 0
lastID = '-2'

fringeUsers = []
last = 0
for val in bgwords:
	numFringe = 0
	for x in range(last, val[1]):
		if labels[x] == -1:
			numFringe = numFringe + 1
	if numFringe / (val[1] - last) >= 0.3:
		userF.write(str(val[0]) + '\n')
	else:
		userNF.write(str(val[0]) + '\n')


for pointD in points:
	if labels[i] == -1:
		pl.plot(pointD[0], pointD[1], 'o', markerfacecolor='k', markeredgecolor='k', markersize=4)
	else:
		pl.plot(pointD[0], pointD[1], 'o', markerfacecolor='b', markeredgecolor='b', markersize=4)
	i = i + 1	

userF.close()
userNF.close()
pl.show()


