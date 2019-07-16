#!/usr/bin/env python                                                                                                                                        

import os
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--directory", help="dir where rootfile files exist")

args = parser.parse_args()

if args.directory:
    directory=args.directory
else:
    print "need --directory option"
    exit()



os.chdir(directory)
ROOTFILES=glob.glob('HISTO__*__*.root')


ngroup=(len(ROOTFILES)//500) +1

print "ngroup", ngroup

groupfiles=[]
for i_group in range(0,ngroup):
    this_group_list=[]
    
    for  i_file in range(0,len(ROOTFILES)):
        if i_file%ngroup==i_group:
            this_group_list.append(ROOTFILES[i_file])

    #print "[Nfile of a group]=",len(this_group_list)
    os.system('hadd -f temp__'+str(i_group)+'.root '+' '.join(this_group_list) )
    groupfiles.append('temp__'+str(i_group)+'.root')
    #print 'temp__'+str(i_group)+'.root'


#print 'hadd -f histoset.root '+' '.join(groupfiles)    
os.system('hadd -f histoset.root '+' '.join(groupfiles) )
#os.system('hadd -f histoset_1.root '+' '.join(groupfiles[1::2]) )
#os.system('hadd -f histoset_2.root '+' '.join(groupfiles[::2]) )


for groupfile in groupfiles:
    os.system('rm '+groupfile)



