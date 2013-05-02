import urllib2
import urllib
import json
import time

def URLRequest(url, params, method="GET"):
    if method == "POST":
        return urllib2.Request(url, data=urllib.urlencode(params))
    else:
	return urllib2.Request(url + "?" + urllib.urlencode(params))

#ins = open("testtweet.dat","r")
#ins = open("dctweet.15.dat","r")
#ins = open("nytweet.15.dat","r")
ins = open("training_set_users.txt", "r")
#ins = open("sstweet.dat","r")
outs = open("training_set.dat","w")
#set_outs = open("ny27_1_uid.dat", "w")
#set_ins = open("ny27_0_uid.dat", "r")

f_proxies = open("proxies.json","r")

proxies = json.load(f_proxies)
#!/usr/bin/python
openers = list()

#add me to the openers list
openers.append(urllib2.build_opener())

#build all of the proxy openers
for item in proxies:
        proxy_handler = urllib2.ProxyHandler(item)
        openers.append(urllib2.build_opener(proxy_handler))
uid_set = set()

#count = 150
proxind = 0

for line in ins:
        #print line
        #obj = json.loads(line)
        #uid = obj[u'user'][u'id']
        uid = line.strip()
        if uid not in uid_set:
                # set_outs.write(str(uid) + '\n')
                uid_set.add(uid)
                suc = False
                while suc == False:
                        try:
                                ret = openers[proxind].open("https://api.twitter.com/1/statuses/user_timeline.json?include_entities=false&include_rts=false&user_id="+str(uid)+"&count=200", None, 12)
                                
                                suc = True
                        except urllib2.HTTPError, e:
                                #print(str(proxind) + "\n")
                                #sys.stdout.flush()
                                # set_outs.flush()
                                outs.flush()
                        except urllib2.URLError, e:
                                print e.args

                        if suc == False:
                                proxind = proxind + 1
                                if proxind == len(openers):
                                        # set_outs.flush()
                                        time.sleep(10)
                                        proxind = 0

                                
                tweets = json.load(ret)
                #loop over tweets
                for tweet in tweets:
                        outs.write(uid + '\t' + ' '.join(tweet[u'text'].rstrip().split()) + '\n')
                        #outs.write(tweet[u'text'].encode('ascii', 'ignore') + '\n')
                #count = count - 1
                #if count == 0:
                #	time.sleep(3600)


ins.close()
outs.close()
#set_outs.close()
#set_ins.close()
