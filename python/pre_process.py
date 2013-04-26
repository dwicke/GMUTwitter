'''
Created on Apr 25, 2013

@author: Indranil
'''
#globals
MIN_USER_CUTOFF = 320
WORD_LENGTH_CUTOFF = 3
#words containing these characters are ignored
BAD_CHAR_SET = set('1234567890%^*()+~<>?^.;:/\\|{}[]@')

import codecs
from Tweet_Data import TwitterData

tweetData = TwitterData()
tweetData.twitterDataSetup('training_set_users.txt', 'training_set_tweets.txt', MIN_USER_CUTOFF)

print(len(tweetData.prunedLocationDict.items()))


#load noise words
stop_word_file = codecs.open('stop.dat', 'r', 'utf-8')
stop_word_list = []
#for line in stop_word_file:
#    stop_word_list.append("".join(i for i in line if  not (ord(i) == 10 or ord(i) == 13)))
#verbs file
verbs_file = codecs.open('verbs.dat', 'r', 'utf-8')
#adverbs file
adverbs_file = codecs.open('adverbs.dat', 'r', 'utf-8')
#build the list
for line in stop_word_file:
    word = "".join(i for i in line.strip())
    if word not in stop_word_list:
        stop_word_list.append(word)
        
#use it at your own risk
'''
for line in verbs_file:
    word = "".join(i for i in line.strip())
    if word not in stop_word_list:
        stop_word_list.append(word)
for line in adverbs_file:
    word = "".join(i for i in line.strip())
    if word not in stop_word_list:
        stop_word_list.append(word)'''

#print(stop_word_list)

#prune the tweets
file_writer = open('words.dat', 'w')

for usrID, usr in tweetData.userIDDict.items():
    for tweet in usr.tweets:
        s = " ".join(word for word in tweet.split() if word.lower() not in stop_word_list)
        pruned = []
        for word in s.split():
            word = word.strip('\n\r!,_').replace("'", "").replace('\"','')
            if len(word) > WORD_LENGTH_CUTOFF and not any((c in BAD_CHAR_SET) for c in word):
                parts = word.split("-",1)
                pruned.extend(part for part in parts if len(part) > WORD_LENGTH_CUTOFF)
        if pruned:
            file_writer.write(str(usr.location).strip() + '\t' + " ".join(pruned) + '\n')

file_writer.close()
