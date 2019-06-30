#!/usr/bin/env python

import argparse
import os


parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--exe", help="executable file")



args = parser.parse_args()

if args.exe:
    exe=args.exe
else:
    print "need --exe option"
    exit()



name='submit__'+''.join(exe.split('.sh')[:-1])
#print 'jds='+name
f=open(name+'.jds','w')

f.write('executable ='+exe+'\n')
f.write('universe   = vanilla\n')
f.write('arguments  = $(Process)\n')
f.write('accounting_group=group_cms\n')
f.write('log = '+name+'.log\n')
f.write('getenv     = True\n')
f.write('output = '+name+'_$(Process).out\n')
f.write('error = '+name+'_$(Process).err\n')
HOSTNAME=os.getenv('HOSTNAME')
if 'ui10' in HOSTNAME:
    f.write('requirements = ( HasSingularity == true )\n')
    f.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest"\n')
    f.write('+SingularityBind = "/cvmfs, /cms, /share"\n')
f.write('queue')
f.close()


#os.system('condor_submit '+name+'.jds > '+name+'.jid')

