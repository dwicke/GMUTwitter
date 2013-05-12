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
    if float(prob) > 0.4 and float(ratio) > 0.5 and len(word) > 2: ## only use words that have a > %50 chance of being local
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
labels = open('labels.txt', 'w')

locationBaseStats = []
idx = 0
userCount = 0
for (userId, user) in tweetData.userIDDict.items():
    count = getCounter()
    allTweets = " ".join(user.tweets) # join all of the user's tweets
    tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
    count.update(tokenized) # make the bag of words for the user any word not in the dict means not present
    if len(count - getCounter()) > 0:
        print user.location + '\t' + str(count.most_common(3))
        labels.write(user.location.strip() + '\n')
        [data.write("{0}\t".format(count[word])) for word in localDict.iterkeys()]
        data.write('\n')
        idx += 1
    userCount += 1
    
print "Wrote {0} users and dropped {1}".format(idx, userCount - idx)
