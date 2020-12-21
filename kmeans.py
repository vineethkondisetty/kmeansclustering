import math
import numpy as np
import pandas as pd
import csv

file1=open('iris.data')
In_text = csv.reader(file1,delimiter = ',')
 
file2 =open('iris.csv','w')
out_csv = csv.writer(file2)
out_csv.writerow(['SepalLength','SepalWidth','PetalLength','PetalWidth','Species']) 
file3 = out_csv.writerows(In_text) 
file1.close()
file2.close()
k=3;
df = pd.read_csv("iris.csv")
f1 = df['SepalLength'].values
f2 = df['SepalWidth'].values
f3 = df['PetalLength'].values
f4 = df['PetalWidth'].values
species = df['Species'].values
original_data = np.array(list(zip(species, f1, f2, f3, f4)))
data = np.array(list(zip(f1, f2, f3, f4)))
datalength=len(data)

def eucliddistance(a, b):
    sum = 0
    zipdata = zip(a,b)
    for x, y in zipdata:
        a = pow((x - y),2)
        sum = sum + a
        eucdist =  math.sqrt(sum)
    return eucdist

def disttable(initial_centroids): 
    distlist = []  
    for x in initial_centroids:
        temp = []
        for y in data:
            temp.append(eucliddistance(x, y))
        distlist.append(temp)
    return distlist

def initial_posc(data):
    randomlistcentroid = []    
    randomlist = np.random.randint(1, datalength, 3)    
    lens = len(randomlist)
    lensets = len(set(randomlist))
    while (lens != lensets):
        randomlist = np.random.randint(1, datalength, 3)
    for i in randomlist:
        randomlistcentroid.append(data[i])
    return randomlistcentroid


def newcentroid(initial_centroids, cluster_table):
    lencentroids = len(initial_centroids)
    for x in range(lencentroids):
        cluster_tablelen = len(cluster_table[x])
        if (cluster_tablelen > 0):
            temp = []
            
            for j in cluster_table[x]:
                temp.append(list(data[j]))
            
            sum = [0] * len(initial_centroids[x])
            for k in temp:
                sum = [(a + b) for a, b in zip(sum, k)]
            initial_centroids[x] = [p / len(temp) for p in sum]
            
    return initial_centroids

def clustertable(dist_table):
    lendisttable=len(dist_table)
    lendist_table1=len(dist_table[0])
    clusterslist = []
    for x in range(0,3):
        clusterslist.append([])   
    for i in range(lendist_table1):
        datapoints = []
        for j in range(lendisttable):
            datapoints.append(dist_table[j][i])
        clusterslist[datapoints.index(min(datapoints))].append(i)
    return clusterslist



# 1000 iterations K means Clustering
   
distancemembers = []
clustermembers = []
initial_centroids = initial_posc(data) 
distance_table = disttable(initial_centroids) 
cluster_table = clustertable(distance_table)
newCentroids = newcentroid(initial_centroids, cluster_table)
distancemembers.append(distance_table)
clustermembers.append(cluster_table)

  
for i in range(1000):
    distance_table = disttable(newCentroids)
    cluster_table = clustertable(distance_table)
    newCentroids = newcentroid(newCentroids, cluster_table)
    distancemembers.append(distance_table)
    clustermembers.append(cluster_table)
    
    if len(distancemembers) > 10:
        distancemembers.pop(0)
        clustermembers.pop(0)
        c2 = all(y == clustermembers[0] for y in clustermembers)
        if c2:
            print("Number of iterations before stopping: ", i)
            break

lennewcentroids =len(newCentroids)
for i in range(lennewcentroids):
    print("Centroid", i, ": ", newCentroids[i])
    print("Members of the cluster: ")
    for j in range(len(cluster_table[i])):
        print(original_data[cluster_table[i][j]])


