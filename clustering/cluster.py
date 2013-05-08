import sys
import numpy as np
import random
import math

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

def assign(features, c):
    assignment = np.zeros(features.shape[0])
    fidx = 0
    for featureSet in features:
        dis = None
        cluster = 0
        print "F: " + str(featureSet)
        for centriod in c:
            distc = distance(featureSet, centriod)
            print "\tD:" + str(distc) + " c:" + str(centriod) 
            if dis == None or dis > distc:
                dis = distc
                assignment[fidx] = cluster
            cluster += 1
        fidx += 1
    return assignment

def update(features, assignment):
    centroids = np.zeros((2,2))
    count = np.array([0,0])
    idx = 0
    for a in assignment:
        centroids[a,0] += features[idx,0]
        centroids[a,1] += features[idx,1]
        count[a] += 1
        idx += 1
    # compute centriods, if there are any empty assign them to random point in feature set 
    return [[ctr/c for ctr in centroid] if not c == 0 else features[random.randint(0,features.shape[0]-1)] for (centroid,c) in zip(centroids,count)]

def main():
    data = open(sys.argv[1], 'r')
    f = np.genfromtxt(data, delimiter=" ")
    print f
    print f.shape
    numclusters = 2
    c1 = random.randint(0,f.shape[0]-1)
    c2 = random.randint(0,f.shape[0]-1)
    print "Intializing with " + str(f[c1]) + " and " + str(f[c2])
    centriods = [f[c1], f[c2]]
    assignment = []
    converged = False
    interation = 0
    while not converged:
        print "Iteration " + str(interation)
        newAssign = assign(f, centriods)
        # Test to see if our assignments are the same as before
        if np.array_equal(newAssign, assignment):
            converged = True
        centriods = update(f, newAssign)
        print "New centroids " + str(centriods)
        assignment = newAssign
        interation += 1
    print assignment

if __name__ == "__main__":
    main()