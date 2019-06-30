#!/usr/bin/env python

import os
import argparse


##Make Fragment##

def make_fragment(tag,fragment,gridpack,nevent,seed):
    if os.getenv('CMSSW_BASE'):
        CMSSW_BASE=os.getenv('CMSSW_BASE')
    else: exit()

    f=open(fragment,'r')
    lines=f.readlines()
    PYTHON_DIR=CMSSW_BASE+'/src/Configuration/Generator/python/'
    fnew=open(PYTHON_DIR+tag+'_cfg.py','w')
    
    fnew.write('import FWCore.ParameterSet.Config as cms\n\
externalLHEProducer = cms.EDProducer(\'ExternalLHEProducer\',\n \
args = cms.vstring(\''+gridpack+'\'),\n\
nEvents = cms.untracked.uint32(5000),\n\
numberOfParameters = cms.uint32(1),  \n\
outputFile = cms.string(\'cmsgrid_final.lhe\'),\n\
scriptName = cms.FileInPath(\'GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh\')\n\
)\n')
    for line in lines:
        fnew.write(line)

    f.close()
    fnew.close()
    #f=open('run_cmsDriver.sh','w')
    command='cmsDriver.py Configuration/Generator/python/'+tag+'_cfg.py --fileout file:OUTPUT.root --mc --eventcontent RAWSIM,LHE --datatier GEN-SIM,LHE --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename '+tag+'_run_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed='+seed+' -n '+nevent+' || exit $? ; '
    
    
    os.system(command)






parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--tag", help="name of this job")
parser.add_argument("--fragment", help="fragment file")
parser.add_argument("--nevent", help="# of events for this job")
parser.add_argument("--gridpack", help="gridpack path for this job")
parser.add_argument("--seed", help="seed number")


args = parser.parse_args()

if args.fragment:
    fragment=args.fragment
else:
    print "need --fragment option"
    exit()
if args.nevent:
    nevent=args.nevent
else:
    print "need --nevent option"
    exit()

if args.seed:
    seed=args.seed
else:
    print "need --seed option"
    exit()

if args.tag:
    tag=args.tag
else:
    print "need --tag option"
    exit()

if args.gridpack:
    gridpack=args.gridpack
else:
    print "need --gridpack option"
    exit()







make_fragment(tag,fragment,gridpack,nevent,seed)
