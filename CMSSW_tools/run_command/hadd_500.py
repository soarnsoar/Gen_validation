#!/usr/bin/env python                                                                                                                                                            \
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
ROOTFILES=glob.glob('*.root')


ngroup=(len(ROOTFILES)//500) +1

print "ngroup", ngroup

groupfiles=[]
for i_group in range(0,ngroup):
    this_group_list=[]
    
    for  i_file in range(0,len(ROOTFILES)):
        if i_file%ngroup==i_group:
            this_group_list.append(ROOTFILES[i_file])


    os.system('hadd -f temp__'+str(i_group)+'.root '+' '.join(this_group_list) )
    groupfiles.append('temp__'+str(i_group)+'.root')


os.system('hadd -f histoset.root '+' '.join(groupfiles) )


for groupfile in groupfiles:
    os.system('rm '+groupfile)



