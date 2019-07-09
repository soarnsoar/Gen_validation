#!/bin/bash


export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_15_patch2/src ] ; then 
 echo release CMSSW_10_2_15_patch2 already exists
else
scram p CMSSW CMSSW_10_2_15_patch2
fi
cd CMSSW_10_2_15_patch2/src



eval `scram runtime -sh`

while [ 1 ];do
    if [ -d Configuration/Generator ];then
	break
    fi
    git-cms-addpkg Configuration/Generator

done

scram b
cd ../../


