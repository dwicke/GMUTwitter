from collections import Counter
from twitterdata import TwitterData
from twitterdata import TwitterUser
import codecs

tweetData = TwitterData()
tweetData.twitterDataSetup('../training_set_users.txt', '../training_set_tweets.txt', 1000)
print 'printing stats'
tweetData.printStats()
print 'done'

## word\tprobability 
f = codecs.open('fetr.dat', u'r', u'utf-8')
localDict = {}

for line in f:
    word, ratio, prob = line.split(u'\t', 2)
    if float(prob) > 0.5: ## only use words that have a > %50 chance of being local
        localDict[word] = float(prob)
    
print len(localDict)

def getCounter():
    cur = Counter()
    for word in localDict.iterkeys():
        cur[word] = 0
    return cur
    
def my_tokenizer(s):
    tokens = []
    for tok in s.split():
        if tok in localDict:
            tokens.append(tok)
    return tokens


data = open('data.txt', 'w')

locationBaseStats = []
idx = 0
for (userId, user) in tweetData.userIDDict.items():
    count = getCounter()
    allTweets = " ".join(user.tweets) # join all of the user's tweets
    tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
    count.update(tokenized) # make the bag of words for the user any word not in the dict means not present
    print user.location + '\t' + str(count.most_common(3))
    data.write(user.location.strip())
    [data.write("\t{0}".format(count[word])) for word in localDict.iterkeys()]
