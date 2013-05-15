import sys
import numpy as np
import json
import math
from collections import Counter

def euclidian(a,b):
    ret = 0
    for (x,y) in zip(a,b):
        ret += (x-y)**2
    return math.sqrt(ret)

def distance(a, b):
    return euclidian(a,b)

def classhelper(tree, data, current):
    (labels, centroids) = tree[current]
    dis = None
    cluster = 0
    assignment = None
    for centriod in centroids:
        distc = distance(data, centriod)
        if dis == None or dis > distc:
            dis = distc
            assignment = cluster
        cluster += 1
    if current + str(assignment) in tree:
        return classhelper(tree, data, current + str(assignment))
    else:
        return labels

def classify(tree, data):
    return classhelper(tree, data, 'root')

def main():
    tree = json.load(open(sys.argv[1],'r'))
    data = open(sys.argv[2], 'r')
    output = open('results.txt', 'w')
    labelsFile = open(sys.argv[3], 'r')
    labels = []
    for x in labelsFile:
        labels.append(x.strip())
    f = np.genfromtxt(data, delimiter="\t")
    index = 0
    total = Counter()
    corr = Counter()
    corr2 = Counter()
    for test in f:
        city = labels[index]
        output.write(city)
        output.write('\t')
        results = classify(tree, test)
        c = Counter()
        c.update(results)
        total[city] += 1
        if city == c.most_common(1)[0][0]:
            corr[city] += 1
        if city == c.most_common(2)[1][0]:
            corr2[city] += 1
        output.write(str(c))
        output.write('\n')
        index += 1
        
    stats = open('stats.txt','w')
    stats.write(str(total))
    stats.write('\n')
    stats.write(str(corr))
    stats.write('\n')
    stats.write(str(corr2))
if __name__ == "__main__":
    main()
