
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

locationBaseStats = []
idx = 0
for location, usrList in tweetData.prunedLocationDict.items():
	locationBaseStats.append([])
	cur = Counter()
	for usr in usrList:
		allTweets = " ".join(usr.tweets) # join all of the user's tweets
		tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
		cur.update(tokenized) # make the bag of words for the user any word not in the dict means not present
	for word in list(localDict):
		weight = (cur[word] * localDict[word] )
		locationBaseStats[idx].append(weight)
	# normalize the array
	pts = np.array(locationBaseStats[idx])
	pts /= np.linalg.norm(pts, ord=1)
	locationBaseStats[idx] = pts
	idx += 1


distPoints = []
ids = []
# now do the users and compare their normalized array to each of the
# cities and and find the two smallest distances and those are the x,y coords

for usrID, usr in tweetData.userIDDict.items():
	allTweets = " ".join(usr.tweets) # join all of the user's tweets
	tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
	c = Counter(tokenized) # make the bag of words for the user any word not in the dict means not present
	userFreq = []
	for word in list(localDict):
		weight = float(c[word] * localDict[word])
		userFreq.append(weight)
	npUserFreq = np.array(userFreq)
	userFreq = npUserFreq / np.linalg.norm(npUserFreq, ord=1) 
	# now find the distances between the cities
	avgDistTop = -1.0
	avgDistSec = -1.0
	for spread in locationBaseStats:
		dist = float(np.sum(np.absolute(spread - userFreq))) 
		if avgDistTop == -1:
			avgDistTop = dist
		elif dist < avgDistTop:
			avgDistTop = dist
		elif avgDistSec == -1:
			avgDistSec = dist
		elif dist < avgDistSec:
			avgDistSec = dist
		
	distPoints.append([avgDistTop, avgDistSec])
	ids.append(usrID)


import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()
userID = open('usrID.dat','w')
userPT = open('usrPT.dat','w')

idIDX = 0
for pointk in distPoints:
	pl.plot(pointk[0], pointk[1], 'o', markerfacecolor='k', markeredgecolor='k', markersize=4)
	userID.write(str(ids[idIDX]) + '\n')
	userPT.write(str(pointk[0]) + '\t' + str(pointk[1]) + '\n')
	idIDX = idIDX +1
	
userID.close()
userPT.close()

pl.show()


