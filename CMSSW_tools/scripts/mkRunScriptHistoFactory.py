#!/usr/bin/env python
import argparse
import os


parser = argparse.ArgumentParser()
####Set options###                                                                                                                             
parser.add_argument("--tag", help="name of this job")
parser.add_argument("--nevent", help="# of events for this job")
parser.add_argument("--seed", help="seed number")


args = parser.parse_args()


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

    exit()
name='run_HistoFactory_'+tag+'__'+seed+'__'+nevent+'evt_cfg'

os.system('mkdir -p '+'JOBDIR_HistoFactory__'+tag+'__'+nevent+'evt/')
os.chdir('JOBDIR_HistoFactory__'+tag+'__'+nevent+'evt/')
f=open(name+'.sh','w')
if os.getenv('CMSSW_BASE'):
    CMSSW_BASE=os.getenv('CMSSW_BASE')
else: exit()
f_userconfig=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/user_config.py')
exec(f_userconfig)
f_userconfig.close()
'''
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
export X509_USER_PROXY=/cms/ldap_home/jhchoi/.proxy
voms-proxy-info
export SCRAM_ARCH=slc7_amd64_gcc700
source $VO_CMS_SW_DIR/cmsset_default.sh


'''
f_histoconfig=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/HistoConfigForReweight.py')
exec(f_histoconfig)
f_histoconfig.close()

#f=open(MYWORKDIR+'/JOBDIR__HistoFactory_'+tag+'__'+nevent+'evt/run_HistoFactory_'+tag+'__'+seed+'__'+nevent+'.sh')
#INPUTDIR=XROOTD_ADDRESS+'/'+MYSTORAGEPATH+'/OUTPUTS__GENEVT_'+tag+'__'+nevent+'/'
INPUTDIR=MYSTORAGEPATH.replace('xrd','/')+'/OUTPUTS__'+tag+'__'+nevent+'/'
inputrootfile=INPUTDIR+'/OUTPUT_'+seed+'.root'
#inputrootfile=MYSTORAGEPATH.replace('/xrd/','/')+'/OUTPUTS__GENEVT_'+tag+'__'+nevent+'/'


#src/Gen_validation/CMSSW_tools/plugins
f.write('#!/bin/bash\n')
f.write('StartTime=$(date +%s)\n')
f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
f.write('export SCRAM_ARCH='+os.getenv('SCRAM_ARCH')+'\n')
f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
#f.write('cd '+CMSSW_BASE+'/src\n')
f.write('echo "==Extract Tarball=="\n')
f.write('tar -xf INPUT__submit__'+name+'.tar.gz\n')
f.write('cd CMSSW'+CMSSW_BASE.split('CMSSW')[-1]+'/src\n'   )
f.write('scram build ProjectRename\n')
f.write('eval `scramv1 runtime -sh`\n')
#f.write('cd ../../\n')
f.write('cd $CMSSW_BASE/src/Gen_validation/CMSSW_tools/plugins\n')
#f.write('CreateCmsRunWeightChecker.py --rootfile '+inputrootfile+'\n')
#f.write('cmsRun RunWeightChecker.py > WeightInfo.txt\n')
f.write('CreateModuleBasedOnConfig.py --config $CMSSW_BASE/src/Gen_validation/CMSSW_tools/scripts/HistoConfigForReweight.py --rootfile '+inputrootfile+'\n')
f.write('cd $CMSSW_BASE/../\n')
f.write('CreateCmsRunPythonBasedOnConfig --config $CMSSW_BASE/src/Gen_validation/CMSSW_tools/scripts/HistoConfigForReweight.py --rootfile '+inputrootfile+'\n')
f.write('cd $CMSSW_BASE/src;scram b -j 10\n')
f.write('cd $CMSSW_BASE/../\n')
for key in HistoConfig:
    f.write('cmsRun RunHistoFactory__'+key+'__.py\n')
f.write('EndTime=$(date +%s)\n')
f.write('echo "runtime : $(($EndTime - $StartTime)) sec"\n')
f.write('echo "@@JOB FINISHED@@"\n')
#f.write('mv *.root '+MYWORKDIR+'/JOBDIR__'+tag+'__'+nevent+'evt/\n')
f.write('xrdfs '+XROOTD_ADDRESS+' mkdir '+MYSTORAGEPATH+'/HISTOS__'+tag+'__'+nevent+'\n')
f.write('xrdcp *.root '+XROOTD_ADDRESS+'/'+MYSTORAGEPATH+'/HISTOS__'+tag+'__'+nevent+'/\n')
f.close()


os.system('chmod u+x '+name+'.sh')
