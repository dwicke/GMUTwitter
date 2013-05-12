import sys
import numpy as np
import random
import math
from Queue import Queue, Empty
from threading import Thread

NUM_THREADS = 2

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

class Worker(Thread):
    def __init__(self, queue, assignment, centroids):
        Thread.__init__(self)
        self.queue = queue
        self.centroids = centroids
        self.assignment = assignment
    
    def run(self):
        try:
            while not self.queue.empty():
                (fidx, featureSet) = self.queue.get(True, .001)
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
        except Empty:
            pass

def assign(features, c):
    assignment = np.zeros(features.shape[0])
    
    queue = Queue()
    fidx = 0
    for featureSet in features:
        queue.put((fidx, featureSet))
        fidx = fidx + 1
    
    workers = []
    for x in xrange(NUM_THREADS):
        workers.append(Worker(queue, assignment, c))
        
    for w in workers:
        w.start()
        
    for w in workers:
        w.join()
    
    return assignment

def update(features, assignment, numclusters):
    centroids = np.zeros((numclusters,2))
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
    centroids = np.zeros((numclusters, 2))
    for x in xrange(0,numclusters):
        centroids[x] = data[random.randint(0,data.shape[0]-1)]
    print "Initializing with centroids:\n" + str(centroids)
    assignment = []
    converged = False
    interation = 0
    while not converged:
        print "Iteration " + str(interation)
        newAssign = assign(data, centroids)
        # Test to see if our assignments are the same as before
        if np.array_equal(newAssign, assignment):
            converged = True
        centroids = update(data, newAssign, numclusters)
        print "New centroids " + str(centroids)
        assignment = newAssign
        interation += 1
    return (assignment, centroids)

def makeTree(tree, data, numclusters, MaxDepth, name):
    if MaxDepth == 0:
        return
    (assignment, centroids) = cluster(data, numclusters)
    tree[name] = centroids
    
    for x in xrange(numclusters):
        indx = 0
        d = []
        for a in assignment:
            if a == x:
                d.append(data[indx])
            indx = indx + 1
        makeTree(tree, np.array(d), numclusters, MaxDepth-1, name+str(x))

def main():
    data = open(sys.argv[1], 'r')
    f = np.genfromtxt(data, delimiter=" ")
    numclusters = int(sys.argv[2])
    MaxDepth = int(sys.argv[3])
    print f
    print f.shape
    tree = dict()
    makeTree(tree, f, numclusters, MaxDepth, 'root')
    print tree

if __name__ == "__main__":
    main()