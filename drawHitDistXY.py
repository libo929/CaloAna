#!/usr/bin/env python

import sys
import math

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
        return -1.

    #mcpEnergy = []

    for mcp in mcps.values():
        vx.append( [mcp[2], mcp[3], mcp[4]] )
        ep.append( [mcp[5], mcp[6], mcp[7]] )
        #mcpEnergy.append(mcp[1])
        #print('PDG ', mcp[0], ', E: ', mcp[1])

    dx = ep[0][0] - ep[1][0]
    dy = ep[0][1] - ep[1][1]
    dz = ep[0][2] - ep[1][2]

    dxy = math.sqrt(dx * dx + dz * dz)
    #print(dxy)

    return dxy



if __name__=='__main__':
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
	
        if len(sys.argv) == 1:
            fileName = "ecal_pi0_50GeV.npz"

        A = np.load(fileName, allow_pickle=True)
        evts = A['CaloEvts']

        dxys = []

        for evt in evts:
            print('Event: ', evt['evtNum'])
            dxy = drawEvent(evt)

            if dxy > 0:
                dxys.append( dxy )

        dxyArr = np.array( dxys )

        plt.hist(dxyArr, range=(6, 12), bins=100, color='b')

        #fig = plt.gcf()
        #fig.savefig('fig.pdf', format='pdf', dpi=1000)

        plt.show()
