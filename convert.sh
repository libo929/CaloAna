#!/usr/bin/env bash

mkdir -p ems

pdg=22

for p in 1 2 3 4 6 7 8 9; do
#for p in 5 10 15 20 25 30 35 40 45 50 55 60 70 80 90 100 110 120; do
	python lcio2npz4ecal.py /media/libo/ssd2/ILDECAL/ECALREC/rec_PDG${pdg}_${p}GeV_REC.slcio
	mv ecal.npz ems/ems_PDG${pdg}_${p}GeV.npz
done
