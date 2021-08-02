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
def drawEvent(evt):
    #----------------mcp---------------------------
    mcps = evt['mcp']

    vx = [] # vertex
    ep = [] # endpoint

    if len(mcps)!=2:
        print('#MCP is not 2, return')
        return

    mcpEnergy = []

    for mcp in mcps.values():
            vx.append( [mcp[2], mcp[3], mcp[4]] )
            ep.append( [mcp[5], mcp[6], mcp[7]] )
            mcpEnergy.append(mcp[1])
            print('PDG ', mcp[0], ', E: ', mcp[1])

    maxMcpEnergy = np.max(np.array(mcpEnergy))
    #print('max: ', maxMcpEnergy)

    #----------------------------------------------

    fig = plt.figure(figsize=(12, 8))

    hitPosEn = evt['hitPosEn']

    X = []
    Y = []
    Z = []
    E = []
    ER = []

    for hpe in hitPosEn:

        if hpe[3] < 0.0:
            continue
       
        #print('---', hpe[0], hpe[1], hpe[2], hpe[3])
        X.append(hpe[0]) # x
        Y.append(hpe[1]) # y
        Z.append(hpe[2]) # z
        E.append(hpe[3]) # calibrated hit energy
                         # hpe[4] : layer

        hitCont = hpe[5]

        er = 0. # hit energy ratio of the MCP having the max energy

        for mcpe, ehit in hitCont.items():
            #print('     --->', mcpe, ehit)
            if mcpe == maxMcpEnergy: 
                er += ehit/hpe[3]

        if hpe[4] > 19:
            er *= 2.

        ER.append(er)

    xArr = np.array(X)
    yArr = np.array(Y)
    zArr = np.array(Z)
    eArr = np.array(E)
    erArr = np.array(ER)
    print(np.max(erArr))

    print('# of hits: ', len(E))

    hitsSize = []

    for e in eArr:
        s = 0.
        if e > 0.2: # 60 GeV
        #if e > 0.1-0.1: # 20 GeV

            s = e * 10.

        hitsSize.append(s)


    hitsSizeArr = np.array(hitsSize)
            


    #----------------hit density---------------------------

    axis = fig.add_subplot(111, projection='3d')

    p = axis.scatter(xArr, yArr, zArr, alpha=1, s=hitsSizeArr, c=erArr/np.max(erArr), cmap='rainbow')
    
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
