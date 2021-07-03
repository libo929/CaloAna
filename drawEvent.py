#!/usr/bin/env python

import sys

import numpy as np
from sklearn.neighbors import KDTree

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#########################################
def drawEvent(evt):
    print('Event: ', evt['evtNum'])
    
    fig = plt.figure(figsize=(15, 8))

    hitPosEn = evt['hitPosEn']

    X = []
    Y = []
    Z = []
    E = []

    allHitPos = []

    for hpe in hitPosEn:
        if hpe[3] < 0.0:
            continue
       
        #print('---', hpe[0], hpe[1], hpe[2])
        X.append(hpe[0])
        Y.append(hpe[1])
        Z.append(hpe[2])
        E.append(hpe[3])

        allHitPos.append([hpe[0], hpe[1], hpe[2]])

    xArr = np.array(X)
    yArr = np.array(Y)
    zArr = np.array(Z)
    eArr = np.array(E)

    caloHitsArray = np.array(allHitPos)
    calHitsTree = KDTree(caloHitsArray)
    hitsDensity = calHitsTree.kernel_density(caloHitsArray[:], h=10, kernel='cosine')
    neighborHits = calHitsTree.query_radius(caloHitsArray[:], r=5.)

    print('# of hits: ', len(hitsDensity))

    energyDensities = []

    for i in range(0, len(hitsDensity)):
        #print(caloHitsArray[i], hitsDensity[i], neighborHits[i])
        neighbors = neighborHits[i]

        energyDensity = 0.

        for neighbor in neighbors:
            #print(neighbor, eArr[neighbor])
            energyDensity += eArr[neighbor]

        energyDensities.append(energyDensity)

        #print('------------')
    
    energyDensitiesArray = np.array(energyDensities)   

    thDensity = [0.05, 0.08, 0.1, 0.3, 0.6, 0.8, 1.2, 1.8]

    for threshold in thDensity: 

        xDen = []
        yDen = []
        zDen = []

        for i in range(0, len(hitsDensity)):
            if energyDensities[i] > threshold:
                xDen.append(X[i])
                yDen.append(Y[i])
                zDen.append(Z[i])

        xDenArr = np.array(xDen)
        yDenArr = np.array(yDen)
        zDenArr = np.array(zDen)

        axis = fig.add_subplot(241 + thDensity.index(threshold), projection='3d')

        axis.scatter(xArr, yArr, zArr, alpha=0.05, s=2, c='b')
        axis.scatter(xDenArr, yDenArr, zDenArr, alpha=1, s=3, c='r')
        axis.set_xlabel('x (mm)')
        axis.set_ylabel('y (mm)')
        axis.set_zlabel('z (mm)')
        axis.set_xlim(-200, 200)
        axis.set_ylim(1800, 2100)
        axis.set_zlim(-200, 200)

    #plt.hist(hitsDensity)
    #plt.hist(neighborHits)
    #plt.hist(energyDensitiesArray)
    
    fig = plt.gcf()
    fig.savefig('fig.pdf', format='pdf', dpi=1000)

    plt.show()


if __name__=='__main__':
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
	
        if len(sys.argv) == 1:
            fileName = "ecal_pi0_50GeV.npz"

        A = np.load(fileName, allow_pickle=True)
        evts = A['CaloEvts']
        
        canPrint = False 

        for evt in evts:
            if canPrint:
                print('---> ', evt['evtNum'], evt['hitPosEn'])

            drawEvent(evt)

            text = input('press enter to continue, or any other key to exit ')
     
            if text != '':
                print('exit')
                break
