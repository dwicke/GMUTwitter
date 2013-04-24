import re
import codecs

#make the string work with print() by getting rid of anything that is not ascii
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class TwitterUser :
	uID = ""
	tweets = []
	location = ""
	
class TwitterData :


	# maps uID -> user object
	userIDDict = {}

	# maps location to list of user objects same as those in userIDDict
	prunedLocationDict = {}

	numTweets = 0

	def twitterDataSetup(self, usersPath, tweetsPath) :
		f = codecs.open(usersPath, 'r', 'utf-8')	
		locationDict = {}


		for line in f:
			userID, location = line.split('\t', 1)
			curU = TwitterUser()
			curU.uID = userID
			curU.location = location
			self.userIDDict[userID] = curU
			if location in locationDict:
				lis = locationDict[location]
				lis.append(curU)
			else:
				locationDict[location] = []
				locationDict[location].append(curU)



		f.close()


		#prune the users that are not in cities with more than 500 users
		for location, userList in locationDict.items():
			if len(userList) < 500:
				for curUser in userList:
					if curUser.uID in self.userIDDict: del self.userIDDict[curUser.uID]
			else:
				self.prunedLocationDict[location] = userList
			
			
		#don't use this dictionary anymore
		locationDict.clear()


		f = codecs.open(tweetsPath, 'r','utf-8')

		self.numTweets = 0
		for line in f:
	
			if len(line.split('\t')) == 4: ## it seems like some of the lines are not right so make sure it is good.
				userID, tweetID, tweet, createdAt = line.split('\t', 3)
				if userID in self.userIDDict:
					# remove things that are not ascii so that can print...
					self.userIDDict[userID].tweets.append(removeNonAscii(tweet))
					self.numTweets = self.numTweets + 1

		f.close()
	
	
	def printStats(self) :
		count = 0
		numUsers = 0
		for a, b in self.prunedLocationDict.items():
			if len(b) >= 500:
				#print (a + " " + str(len(b)))
				numUsers = numUsers + len(b)
				count = count + 1
		print(count)
		print(numUsers)	
		print(self.numTweets)