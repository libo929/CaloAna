#!/usr/bin/env bash

pdg=22

for p in 5 10 15 20 25 30 35 40 45 50 55 60 70 80 90 100 110 120 200; do
	python lcio2npz4ecal.py /media/libo/ssd2/ILDECAL/rec_PDG${pdg}_${p}GeV_REC.slcio
	mv ecal.npz ems_PDG${pdg}_${p}GeV.npz
done
