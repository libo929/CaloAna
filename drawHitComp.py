#!/usr/bin/env python

import sys

import numpy as np
from sklearn.neighbors import KDTree

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotMCP(vx, ep, plt):
    for i in range(0, len(vx)):
        x = [ vx[i][0], ep[i][0] ]
        y = [ vx[i][1], ep[i][1] ]
        z = [ vx[i][2], ep[i][2] ]

        plt.plot(x, y, z, linestyle='dotted', color='g')


#########################################
def float2color(zero2one):
    x = zero2one * 256 * 256 * 256
    r = x % 256
    g = ((x - r)/256 % 256)
    b = ((x - r - g * 256)/(256*256) % 256)
    r = round(float(r/256),2)
    g = round(float(g/256),2)
    b = round(float(b/256),2)
    return (r,g,b) 


#########################################
def drawEvent(evt):
    col = float2color(0.1)

    #----------------mcp---------------------------
    mcps = evt['mcp']

    vx = [] # vertex
    ep = [] # endpoint

    if len(mcps)!=2:
        return

    for mcp in mcps.values():
            vx.append( [mcp[2], mcp[3], mcp[4]] )
            ep.append( [mcp[5], mcp[6], mcp[7]] )
            print('PDG ', mcp[0], ', E: ', mcp[1])

    #----------------------------------------------

    fig = plt.figure(figsize=(18, 9))

    hitPosEn = evt['hitPosEn']

    X = []
    Y = []
    Z = []
    E = []

    allHitPos = []

    for hpe in hitPosEn:
        if hpe[3] < 0.0:
            continue
       
        print('---', hpe[0], hpe[1], hpe[2])
        X.append(hpe[0])
        Y.append(hpe[1])
        Z.append(hpe[2])
        E.append(hpe[3])

        hitCont = hpe[5]

        for mcpe, ehit in hitCont.items():
            print('     --->', mcpe, ehit)

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


    #----------------hit density---------------------------
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


    energyDensitiesArrayNorm = energyDensitiesArray / np.max(energyDensitiesArray)


    xDen = []
    yDen = []
    zDen = []

    for i in range(0, len(hitsDensity)):
            xDen.append(X[i])
            yDen.append(Y[i])
            zDen.append(Z[i])

    xDenArr = np.array(xDen)
    yDenArr = np.array(yDen)
    zDenArr = np.array(zDen)

    axis = fig.add_subplot(111, projection='3d')

    p = axis.scatter(xArr, yArr, zArr, alpha=1, s=energyDensitiesArrayNorm*5, 
            c=energyDensitiesArrayNorm, cmap='rainbow')
    
    #mat = np.arange(0,10)
    #cax = axis.matshow(mat, cmap='cool')
    #axis.scatter(xDenArr, yDenArr, zDenArr, alpha=1, s=3, c=)
    fig.colorbar(p)
    axis.set_xlabel('x (mm)')
    axis.set_ylabel('y (mm)')
    axis.set_zlabel('z (mm)')
    axis.set_xlim(-100, 100)
    axis.set_ylim(1760, 2030)
    axis.set_zlim(-100, 100)


    plotMCP(vx, ep, plt)


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

        text = ''

        for evt in evts:
            print('Event: ', evt['evtNum'])

            text = input('press enter to draw event, s to skip, e/q to exit ')

            if text != 'e' and text != 's' and text != 'q':
                drawEvent(evt)

            print('-------------------------------------------------------')
     
            if text == 'e' or text == 'q':
                print('Exit ...')
                break
