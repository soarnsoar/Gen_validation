#!/usr/bin/env python


#--To check runtime

from datetime import datetime

start=datetime.now()

#--Get option


import argparse
import os


parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--conf", help="Confs name to Run")
parser.add_argument('--b',action='store_true')
parser.add_argument('--xtorun',help="variable to run (e.g.) Zmuon_pt")

args = parser.parse_args()
if args.conf:
    ConfToRun=args.conf
else:
    print "need --conf option"
    exit()


ConfigToRun=ConfToRun.split(',')
print '===ConfigToRun==='
print ConfigToRun

import ROOT
import os
import copy

#--Set CMSSW_BASE path
CMSSW_BASE = os.getenv('CMSSW_BASE')

##--Configration
f=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/PlotConfigForReweight.py','r')

exec(f)

##--HistoConfig (to get xname)

f=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/HistoConfigForReweight.py','r')
exec(f)


##--batch job


    
if args.b==True:

    f_userconfig=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/user_config.py')
    exec(f_userconfig)
    f_userconfig.close()

    for config in ConfigToRun:
        for x in HistoConfig:

            os.chdir(MYWORKDIR)
            os.system('mkdir -p '+'JOBDIR__CombineHisto__'+config+'__'+x)
            os.chdir('JOBDIR__CombineHisto__'+config+'__'+x)
            f=open('run__CombinedHisto__'+config+'__'+x+'.sh','w')
            if os.getenv('CMSSW_BASE'):
                CMSSW_BASE=os.getenv('CMSSW_BASE')
            else: exit()

        
            f.write('#!/bin/bash\n')
            f.write('StartTime=$(date +%s)\n')
            f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
            f.write('export SCRAM_ARCH='+os.getenv('SCRAM_ARCH')+'\n')
            f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            #f.write('cd '+CMSSW_BASE+'/src\n')
            f.write('echo "==Extract Tarball=="\n')
            f.write('tar -xf INPUT__submit__run__CombinedHisto__'+config+'__'+x+'.tar.gz\n')
            f.write('cd CMSSW'+CMSSW_BASE.split('CMSSW')[-1]+'/src\n'   )
            f.write('scram build ProjectRename\n')
            f.write('eval `scramv1 runtime -sh`\n')
            f.write('cd ../../\n')
            f.write('CombineHistos.py --conf '+config+' --xtorun '+x+'\n')
            f.write('EndTime=$(date +%s)\n')
            f.write('echo "runtime : $(($EndTime - $StartTime)) sec"\n')
            f.write('echo "@@JOB FINISHED@@"\n')
            f.close()
            os.system('chmod u+x '+'run__CombinedHisto__'+config+'__'+x+'.sh')
            os.system('mkBatch.py --exe run__CombinedHisto__'+config+'__'+x+'.sh')
            #name='submit__'+''.join(exe.split('.sh')[:-1])
            command='condor_submit submit__'+'run__CombinedHisto__'+config+'__'+x+'.jds > submit__'+'run__CombinedHisto__'+config+'__'+x+'.jid'
            print "[JOB Submitted]"+command
            os.system(command)
        exit()
            





#--Set modules path
import sys
sys.path.append(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules')

from GetCombinedHisto import GetCombinedHisto 

##--No Graphical Window

ROOT.gROOT.SetBatch(ROOT.kTRUE)



ROOT.gROOT.LoadMacro(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/GetHisto.C')
ROOT.gROOT.LoadMacro(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/SaveObjectToFile.C')






for config in ConfigToRun:
    print 'config='+config
    this_rwgt_info=rwgt_info[config]
    for proc in this_rwgt_info['process']:
        histopath=this_rwgt_info['process'][proc]['histo_path']
        savepath='/'.join(histopath.split('/')[:-1])+'/combined_histo/'
        os.system('mkdir -p '+savepath)
        for var in this_rwgt_info['variation']:
            print 'var->',var
            combination=this_rwgt_info['variation'][var]['combination']
            name=this_rwgt_info['variation'][var]['name']
            idx_list=this_rwgt_info['variation'][var]['idx']
            
            print 'name->',name
            
            print "====",name,"::",var,"===="
            for x in HistoConfig:

                if args.xtorun:
                    xtorun=args.xtorun
                    if x!=xtorun: continue

                #if x!='Zmuon_pt': continue
                ##x = variable name such as Zmuon_pt
                print ">>>>>",x
                hlist=[]
                for idx in idx_list:
                    h=ROOT.GetHisto(histopath,"DYValidation/"+x+'_'+str(idx))
                    hlist.append(copy.deepcopy(h))
                h_combined=GetCombinedHisto(hlist,combination,name)
                h_statonly=GetCombinedHisto(hlist,'statonly',name)
                
                ROOT.SaveObjectToFile(savepath+'/combined_histo__'+var+'__'+x+'.root',h_combined)
                ROOT.SaveObjectToFile(savepath+'/combined_histo__'+var+'__'+x+'__'+'statonly'+'.root',h_statonly)
                
                #this_rwgt_info['process'][proc]['histogram']=copy.deepcopy(h_combined)
                del hlist
                

#tcanvas =ROOT.TCanvas( "cc", "cc" , 800, 600 )
#h_combined.Draw()
#tcanvas.SaveAs('a.png')
#tcanvas =ROOT.TCanvas( "cc", "cc" , 800, 600 )
#h.Draw()
#tcanvas.SaveAs('a.png')
##Draw variable
#TGraphAsymmErrors
#ROOT.TGraphAsymmErrors()
#fileIn=ROOT.TFile.Open("/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell01234j_5f_LO_MLM__5000evt/combined_histo.root"



print "runtime=",datetime.now()-start
