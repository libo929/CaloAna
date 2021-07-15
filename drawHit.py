#!/usr/bin/env python

#ROOT
import ROOT
from ROOT import TCanvas
from ROOT import TGraph
from ROOT import TGraphErrors
from ROOT import gROOT
from ROOT import TLegend
from ROOT import TFile
from ROOT import TGaxis
from ROOT import gDirectory
from ROOT import gStyle
from ROOT import gPad
from ROOT import TH1F
from ROOT import TF1
from ROOT import TVector3
from ROOT import TEveEventManager

# LCIO
from pyLCIO.io.LcioReader import LcioReader
from pyLCIO import EVENT
from pyLCIO import UTIL

import numpy as np

import sys

#########################################
def drawEvent(evtNum, eveManager, allHitPos):
    ps = ROOT.TEvePointSet()
    ps.SetOwnIds(ROOT.kTRUE)
    ps.SetMarkerSize(1)
    ps.SetMarkerStyle(4)
    ps.SetMarkerColor(2)
    
    evtName = 'event ' + str(evtNum)
    evt = TEveEventManager(evtName, "")
    eveManager.AddEvent(evt)
    
    mm2cm = 0.1
    
    for pos in allHitPos:
        ps.SetNextPoint(pos[0] * mm2cm, pos[1] * mm2cm, pos[2] * mm2cm)
    
    eveManager.AddElement(ps)
    eveManager.Redraw3D()

'''
        #----------------------------------------------
        evt = drawEvent(allHitPos, evtNum)
        text = raw_input('press any key to exit: ')

        if text == '':
            evt.DisableListElements()
        else:
            print('exit')
            break

	return evt
'''

#########################################
def readEvent(evt):
    hitPosEn = evt['hitPosEn']

    allHitPos = []

    for hpe in hitPosEn:
        if hpe[3] < 0.0:
            continue
       
        #print('---', hpe[0], hpe[1], hpe[2])

        #hitCont = hpe[5]

        #for mcpe, ehit in hitCont.items():
        #    print('     --->', mcpe, ehit)

        allHitPos.append([hpe[0], hpe[1], hpe[2]])

    return allHitPos


#-----------------------------------------------------------------------------------------------------------
if __name__=='__main__':
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
	
        if len(sys.argv) == 1:
            fileName = "ems_PDG111_100GeV.npz"
	
	
        print('Loaded file: ', fileName)

        A = np.load(fileName, allow_pickle=True)
        evts = A['CaloEvts']
        eveManager = ROOT.TEveManager.Create()

        for evt in evts:
            evtNum = evt['evtNum']
            print('Event: ', evtNum)

            text = input('press enter to draw event, s to skip, e/q to exit ')

            eventData = readEvent(evt)
            drawEvent(evtNum, eveManager, eventData)

            if text == 'e' or text == 'q':
                print('Exit ...')
                break
