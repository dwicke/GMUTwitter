#!/usr/bin/python

import sys
from pymongo import Connection
import pymongo
import re

"""
    Read the database and writes the tweets to the specified file.
    Returns them in the format userid<tab>tweet
"""

def main():
    out = open(sys.argv[1], 'w')
    conn = Connection(sys.argv[2], 27017)
    db = conn.scraping
    tweets = db.tweets
    print tweets
    users = tweets.find({"last_response": 200}, timeout=False)
    print "Writing user " + str(users.count())
    for user in users:
        print 'Writing user ' + user['index']
        for tweet in user['response']:
            text = re.sub('\W+', ' ', tweet['text'])
            out.write(tweet['user']['id_str'] + '\t' + text + '\n')

if __name__ == "__main__":
    main()