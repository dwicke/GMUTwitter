from collections import Counter
from twitterdata import TwitterData
from twitterdata import TwitterUser
import re
import codecs
# import word\tprobability 
f = codecs.open('testLocal.txt', u'r', u'utf-8')
localDict = {}

for line in f:
	word, prob = line.split(u'\t', 1)
	localDict[word] = float(prob)
	
print localDict

f.close()


def my_tokenizer(s):
	tokens = []
	for tok in s.split():
		if tok in localDict:
			tokens.append(tok)
	return tokens


tweetData = TwitterData()
tweetData.twitterDataSetup('../training_set_users.txt', '../training_set_tweets.txt', 1000)


bgwords = {}

for usrID, usr in tweetData.userIDDict.items():
	allTweets = " ".join(usr.tweets) # join all of the user's tweets
	tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
	bgwords[usrID] = Counter(tokenized) # make the bag of words for the user any word not in the dict means not present
	
for id, bg in bgwords.items():
	print bg
	print '\n'




