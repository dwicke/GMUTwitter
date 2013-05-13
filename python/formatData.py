from collections import Counter
from twitterdata import TwitterData
from twitterdata import TwitterUser
import codecs
from multiprocessing import Queue
from Queue import Empty
import time
from multiprocessing import Pool
from multiprocessing.process import Process
from sets import Set

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

def writer(q):
    data = open('data.txt', 'w')
    labels = open('labels.txt', 'w')
    
    while not q.empty():
        try:
            (loc, count) = q.get(timeout=.5)
        except Empty:
            time.sleep(1)
            
def processor(q, userQ):
    try:
        while not userQ.empty():
            user = userQ.get(timeout=.1)
            count = getCounter()
            allTweets = " ".join(user.tweets) # join all of the user's tweets
            tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
            count.update(tokenized) # make the bag of words for the user any word not in the dict means not present
            if len(count - getCounter()) > 0:
                q.put((user.location, count))
    except Empty:
        return

if __name__ == '__main__':
    locals = Set()
    for x in open('./finalLocals.dat','r'):
        locals.add(x.strip())
    print len(locals)
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
    
    data = open('data.txt', 'w')
    labels = open('labels.txt', 'w')
    
    locationBaseStats = []
    idx = 0
    userCount = 0
    """
    q = Queue()
    
    dataQ = Queue()
    for (userId, user) in tweetData.userIDDict.items():
        dataQ.put(user)
    
    pool = Pool(processes=4)
    result = pool.apply_async(processor, [q, dataQ])
    p = Process(target=writer, args=(q,))
    p.start()
    result.join()
    p.join()
    """
    for (userId, user) in tweetData.userIDDict.items():
        count = getCounter()
        allTweets = " ".join(user.tweets) # join all of the user's tweets
        tokenized = my_tokenizer(allTweets.lower()) # get all of the tokens 
        count.update(tokenized) # make the bag of words for the user any word not in the dict means not present
        if userId in locals and len(count - getCounter()) > 0:
            #print user.location + '\t' + str(count.most_common(3))
            labels.write(user.location.strip() + '\n')
            itr = localDict.iterkeys()
            data.write(str(count[itr.next()]))
            try:
                while True:
                    c = count[itr.next()]
                    if c > 0:
                        data.write("\t1")
                    else:
                        data.write("\t0")
            except StopIteration:
                data.write('\n')
            idx += 1
        userCount += 1
        
    print 'Wrote {0} users and dropped {1}'.format(idx, userCount - idx)
    
