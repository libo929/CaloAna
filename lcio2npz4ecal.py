import numpy as np

# lcio
from pyLCIO.io.LcioReader import LcioReader
from pyLCIO import EVENT
from pyLCIO import UTIL

import sys

def makeEventContent(event):

    #-----------------------------MCP collection---------------------
    mcps = {}
        

    #-----------------------------Hit--------------------------------
    hcalHits = event.getCollection('EcalBarrelCollectionRec')
    evtNum   = event.getEventNumber()

    nHit = hcalHits.getNumberOfElements()
    cellIdEncoding = hcalHits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding ) 
    idDecoder = UTIL.BitField64( cellIdEncoding )

    hitPosEn = []

    for iHit in range(0, nHit):
        caloHit = hcalHits.getElementAt( iHit )
        simCaloHit = caloHit.getRawHit()
        #print('cellID: ', simCaloHit.getCellID0(), simCaloHit.getCellID1(), 'hit energy: ', simCaloHit.getEnergy())

        mcp4HitEnergy = {}

        for i in range(0, simCaloHit.getNMCContributions()):
            mcp = simCaloHit.getParticleCont(i)
            mcpPDG = mcp.getPDG()
            mcpEnergy = mcp.getEnergy()
            hitEnergyCont = simCaloHit.getEnergyCont(i)

            if mcp in mcp4HitEnergy.keys():
               mcp4HitEnergy[mcp] += hitEnergyCont
            else:
               mcp4HitEnergy[mcp] = hitEnergyCont

            #print( '---> contr: %5d' % i, ', MCP PDG: %5d' % mcpPDG, ', MCP energy: %12.5f' % mcpEnergy,
            #            ', hit energy contr: %5e' % hitEnergyCont )

        totalCont = 0.
        hitCont = {}

        for mcp, cont in mcp4HitEnergy.items():
            totalCont += cont
            hitCont[mcp.getEnergy()] = cont

            pdg = mcp.getPDG()
            energy = mcp.getEnergy()
            vertex = mcp.getVertex()
            endpoint = mcp.getEndpoint()
            #print(pdg, energy, vertex[0], vertex[1], vertex[2])

            if not mcp.getEnergy() in mcps.keys():
                mcps[mcp.getEnergy()] = [ pdg, energy, vertex[0], vertex[1], vertex[2], endpoint[0], endpoint[1], endpoint[2] ]


        if totalCont - simCaloHit.getEnergy() > 1.e-6:
            print('warning: hit energy total less than recorded!')

        hitPos = caloHit.getPositionVec()
        hitEnergy = caloHit.getEnergy()
        cellID = int( caloHit.getCellID0() & 0xffffffff ) | ( int( caloHit.getCellID1() ) << 32 )
        idDecoder.setValue( cellID )
        layer = int(idDecoder['layer'])

        hitPosEn.append( [hitPos[0], hitPos[1], hitPos[2], hitEnergy, layer, hitCont] )

        #print('-----------------------------------------------------------------------------------------')

    #print(mcps.keys())
    evtCollection = {'evtNum': evtNum, 'mcp': mcps, 'hitPosEn': hitPosEn}

    return evtCollection

#########################################

def readEvents(reader):
    evtList = []

    for event in reader:
        evtContent = makeEventContent(event)

        if evtContent['evtNum'] > 100000:
            break

        evtList.append(evtContent)

    return evtList


if __name__=='__main__':
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
	
        if len(sys.argv) == 1:
            fileName = "rec_REC.slcio"
	
        reader = LcioReader( fileName )
        print('Loaded file: ', fileName)
	
        anEvtList = readEvents(reader)
        anEvtArray = np.array(anEvtList, dtype=object)
        np.savez('ecal', CaloEvts=anEvtArray)

        A = np.load('ecal.npz', allow_pickle=True)
        evts = A['CaloEvts']
        
        canPrint = False

        if canPrint:
            for evt in evts:
                print('---> ', evt['evtNum'], evt['hitPosEn'])
