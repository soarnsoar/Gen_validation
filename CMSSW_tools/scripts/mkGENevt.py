#!/usr/bin/env python
import argparse
import os


parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--tag", help="name of this job")
parser.add_argument("--fragment", help="fragment file")
parser.add_argument("--nevent", help="# of events for this job")
parser.add_argument("--gridpack", help="gridpack path for this job")
parser.add_argument("--startseed", help="initial seed #")
parser.add_argument("--endseed", help="fin seed #")


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

if args.startseed:
    startseed=args.startseed
else:
    print "need --startseed option"
    exit()

if args.endseed:
    endseed=args.endseed
else:
    print "need --endseed option"
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

if os.getenv('CMSSW_BASE'):
    CMSSW_BASE=os.getenv('CMSSW_BASE')
else: exit()

f_userconfig=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/user_config.py')
exec(f_userconfig)
f_userconfig.close()
#MYWORKDIR

#'run_'+tag+'__'+seed+'__'+nevent+'evt_cfg.sh'
for i in range(int(startseed),int(endseed)+1):
    seed=str(i)
    name='run_'+tag+'__'+seed+'__'+nevent+'evt_cfg'
    os.chdir(MYWORKDIR)
    os.system('mkRunScript.py --fragment '+fragment+' --nevent '+nevent+' --seed '+seed+' --tag '+tag+' --gridpack '+gridpack)
    os.system('mkBatch.py --exe '+name+'.sh')
    print '[JOB SUBMIT]condor_submit '+'submit__'+name+'.jds > submit__'+name+'.jid'
    os.system('condor_submit '+'submit__'+name+'.jds > submit__'+name+'.jid') 
    
