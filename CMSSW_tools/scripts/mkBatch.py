#!/usr/bin/env python

import argparse
import os


parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--exe", help="executable file")
parser.add_argument("--inputfiles", help="input files")



args = parser.parse_args()

if args.exe:
    exe=args.exe
else:
    print "need --exe option"
    exit()
if args.inputfiles:
    inputfiles=args.inputfiles
else:
    inputfiles=''
#    print "need --inputfiles option"
#    exit()


name='submit__'+''.join(exe.split('.sh')[:-1])
#print 'jds='+name

CMSSW_BASE=os.getenv('CMSSW_BASE')

f=open(name+'.jds','w')

f.write('executable ='+exe+'\n')
f.write('universe   = vanilla\n')
f.write('arguments  = $(Process)\n')
f.write('accounting_group=group_cms\n')
f.write('log = '+name+'.log\n')
f.write('getenv     = True\n')
f.write('output = '+name+'_$(Process).out\n')
f.write('error = '+name+'_$(Process).err\n')
f.write('should_transfer_files = YES\n')
#f.write('when_to_transfer_output = ON_EXIT\n')
f.write('transfer_input_files = '+CMSSW_BASE.split('CMSSW')[0]+'/INPUT_TARS/INPUT__'+name+'.tar.gz\n')
#f.write('transfer_output_remaps = "OUTPUT.root = OUTPUT_$(Process).root"\n')
#f.write('transfer_output_files = OUTPUT_'+seed+'.root\n')

HOSTNAME=os.getenv('HOSTNAME')
if 'ui10' in HOSTNAME:
    f.write('requirements = ( HasSingularity == true )\n')
    f.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest"\n')
    f.write('+SingularityBind = "/cvmfs, /cms, /share"\n')
f.write('queue')
f.close()


#os.system('condor_submit '+name+'.jds > '+name+'.jid')




os.chdir(CMSSW_BASE+'/../')
#os.system('rm INPUT__'+name+'.tar.gz')
print '[mkBatch.py]','tar CMSSW....for  ',name
os.system('tar -czf INPUT__'+name+'.tar.gz CMSSW* '+inputfiles)
os.system('mkdir -p INPUT_TARS/')
os.system('mv INPUT__'+name+'.tar.gz INPUT_TARS/')




'''


Ref



        jobname='CombineHisto__'+config+'__'+x
        os.chdir(MYWORKDIR)
        os.system('mkdir -p '+'JOBDIR__'+jobname)
        os.chdir('JOBDIR__'+jobname)
        f=open(jobname+'.sh','w')
        if os.getenv('CMSSW_BASE'):
        CMSSW_BASE=os.getenv('CMSSW_BASE')
        else: exit()


        f.write('#!/bin/bash\n')
        f.write('StartTime=$(date +%s)\n')
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
        f.write('export SCRAM_ARCH='+os.getenv('SCRAM_ARCH')+'\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('echo "==Extract Tarball=="\n')
        f.write('tar -xf INPUT__submit__'+jobname+'.tar.gz\n')
        f.write('cd CMSSW'+CMSSW_BASE.split('CMSSW')[-1]+'/src\n'   )
        f.write('scram build ProjectRename\n')
        f.write('eval `scramv1 runtime -sh`\n')
        f.write('cd ../../\n')
        f.write('CombineHistos.py --conf '+config+' --xtorun '+x+'\n')
        f.write('EndTime=$(date +%s)\n')
        f.write('echo "runtime : $(($EndTime - $StartTime)) sec"\n')
        f.write('echo "@@JOB FINISHED@@"\n')
        f.close()
        os.system('chmod u+x '+jobname+'.sh')
        os.system('mkBatch.py --exe '+jobname+'.sh')
        #name='submit__'+''.join(exe.split('.sh')[:-1])                                                                                                                                                     
        command='condor_submit submit__'+jobname+'.jds > submit__'+jobname+'.jid'
        print "[JOB Submitted]"+command
        os.system(command)




'''
