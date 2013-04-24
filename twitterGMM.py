from twitterdata import TwitterData
from twitterdata import TwitterUser


d = TwitterData()

d.twitterDataSetup('training_set_users.txt', 'training_set_tweets.txt')
d.printStats()