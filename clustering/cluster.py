import sys
import numpy as np
import random
import math
#from Queue import Queue, Empty
from Queue import Empty
from multiprocessing import Queue, Process, Pipe, Pool
#from threading import Thread
import json
import time
import functools

NUM_THREADS = 12

def manhton(a,b):
    ret = 0
    for x,y in a,b:
        ret += abs(x-y)
    return ret

def euclidian(a,b):
    ret = 0
    for (x,y) in zip(a,b):
        ret += (x-y)**2
    return math.sqrt(ret)

def distance(a, b):
    return euclidian(a,b)

# class Worker(Thread):
class Worker(Process):
    def __init__(self, queue, output, assignment, centroids):
        # Thread.__init__(self)
        Process.__init__(self)
        self.queue = queue
        self.centroids = centroids
        self.assignment = assignment
        self.output = output
    
    def run(self):
        try:
            while not self.queue.empty():
                (fidx, featureSet) = self.queue.get(True, .1)
                dis = None
                cluster = 0
                # print "F: " + str(featureSet)
                for centriod in self.centroids:
                    distc = distance(featureSet, centriod)
                    # print "\tD:" + str(distc) + " c:" + str(centriod) 
                    if dis == None or dis > distc:
                        dis = distc
                        self.assignment[fidx] = cluster
                    cluster += 1
                self.output.send((fidx,self.assignment[fidx]))
        except Empty:
            return

def makeWorker(featureSet, centroids):
    dis = None
    assignment = None
    cluster = 0
    for centriod in centroids:
        distc = distance(featureSet, centriod)
        if dis == None or dis > distc:
            dis = distc
            assignment = cluster
        cluster += 1
    return assignment

def assign(features, c):
    result = None
    try:
        pool = Pool(processes=NUM_THREADS)
        result = pool.map(functools.partial(makeWorker, centroids=c), features, chunksize=10)
    except:
        pass
    finally:
        pool.close()
        pool.join()
        return result
    
"""
    assignment = np.zeros(features.shape[0])
    
    queue = Queue()
    output = Queue(10)
    fidx = 0
    for featureSet in features:
        queue.put((fidx, featureSet))
        fidx = fidx + 1
    pipes = []
    workers = []
    for x in xrange(NUM_THREADS):
        workers.append(Worker(queue, assignment, c))
        pipes.append(parent_conn)
        
    for w in workers:
        w.start()
    
    for w in workers:
        w.join()
    
    return assignment
"""

def update(features, assignment, numclusters):
    centroids = np.zeros((numclusters, features.shape[1]))
    count = np.zeros(numclusters)
    idx = 0
    
    for a in assignment:
        centroids[a,0] += features[idx,0]
        centroids[a,1] += features[idx,1]
        count[a] += 1
        idx += 1
    # compute centriods, if there are any empty assign them to random point in feature set 
    # return [[ctr/c for ctr in centroid] if not c == 0 else features[random.randint(0,features.shape[0]-1)] for (centroid,c) in zip(centroids,count)]
    return [[ctr/c for ctr in centroid] if not c == 0 else features[random.randint(0,features.shape[0]-1)] for (centroid,c) in zip(centroids,count)]

def cluster(data, numclusters):
    centroids = np.zeros((numclusters, data.shape[1]))
    for x in xrange(0,numclusters):
        centroids[x] = data[random.randint(0,data.shape[0]-1)]
    # print "Initializing with centroids:\n" + str(centroids)
    assignment = np.zeros(data.shape[0])
    converged = False
    interation = 0
    while not converged:
        
        print "Iteration " + str(interation)
        newAssign = assign(data, centroids)
        # Test to see if our assignments are the same as before
        change = sum(abs(np.subtract(newAssign, assignment)))
        print '\tchanges: ' + str(change)
        if change < 10 or interation > 30:
            converged = True
        centroids = update(data, newAssign, numclusters)
        # print "New centroids " + str(centroids)
        assignment = newAssign
        interation += 1
    return (assignment, centroids)

def makeTree(tree, data, numclusters, MaxDepth, name, labels):
    if MaxDepth == 0 or len(data) == 0:
        return
    (assignment, centroids) = cluster(data, numclusters)
    tree[name] = [labels, centroids]
    
    for x in xrange(numclusters):
        indx = 0
        d = []
        l = []
        for a in assignment:
            if a == x:
                d.append(data[indx])
                l.append(labels[indx])
            indx = indx + 1
        makeTree(tree, np.array(d), numclusters, MaxDepth-1, name+str(x), l)
        
class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
            if isinstance(obj, np.ndarray) and obj.ndim == 1:
                    return [x for x in obj]
            return json.JSONEncoder.default(self, obj)

def main():
    data = open(sys.argv[1], 'r')
    labelsFile = open(sys.argv[2], 'r')
    labels = []
    for x in labelsFile:
        labels.append(x.strip())
    f = np.genfromtxt(data, delimiter="\t")
    numclusters = int(sys.argv[3])
    MaxDepth = int(sys.argv[4])
    print f
    print f.shape
    tree = dict()
    makeTree(tree, f, numclusters, MaxDepth, 'root', labels)
    json.dump(tree, open('cluster.json','w'),cls=NumpyAwareJSONEncoder)

if __name__ == "__main__":
    main()