#!/usr/bin/env python


import argparse
parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--deno_config", help="denominator's configname(mg260LO) ")
parser.add_argument("--deno_proc", help="denominator's procname(dy01234j_LO_MLM), ")
parser.add_argument("--deno_alias", help="denominator's alias (MG260), ")


parser.add_argument("--nume_config", help="numerator's configname(mg261LO) ")
parser.add_argument("--nume_proc", help="numerator'sprocname(dy01234j_LO_MLM), ")
parser.add_argument("--nume_alias", help="numerator's alias(MG261), ")

parser.add_argument('--x' , help='variable name to draw')
parser.add_argument('--var' , help='var name to draw, such as muRmuF')

parser.add_argument('--batch' , action='store_true',help='batch')
parser.add_argument('--yaxis',help='title of yaxis')
parser.add_argument('--yaxis_ratio',help='title of yaxis of ratio')
parser.add_argument('--title', help='title of canvas')
parser.add_argument('--dirname', help='name of DIR to save')

parser.add_argument('--test_stat', help='name of stat test(e.g chi2)')

parser.add_argument('--pvalue_threshold', help='pvalue threshold of of the stat test')

args = parser.parse_args()



if args.deno_config:
    deno_config=args.deno_config
else:
    print "need --deno_config option"
    exit()

if args.deno_proc:
    deno_proc=args.deno_proc
else:
    print "need --deno_proc option"
    exit()

if args.deno_alias:
    deno_alias=args.deno_alias
else:
    print "need --deno_alias option"
    exit()




if args.nume_config:
    nume_config=args.nume_config
else:
    print "need --nume_config option"
    exit()

if args.nume_proc:
    nume_proc=args.nume_proc
else:
    print "need --nume_proc option"
    exit()

if args.nume_alias:
    nume_alias=args.nume_alias
else:
    print "need --nume_alias option"
    exit()


if args.x:
    x=args.x
else:

    print "need --x option"
    exit()

if args.var:
    variation=args.var

else:
    print "need --var option"
    exit()

if args.title:
    title=args.title
else:
    print "--title is needed"
    
if args.yaxis:
    yaxis=args.yaxis
else:
    print "--yaxis is needed"

if args.yaxis_ratio:
    yaxis_ratio=args.yaxis_ratio
else:
    print "--yaxis_ratio is needed"

if args.dirname:
    dirname=args.dirname
else:
    print "--dirname is needed"

if args.test_stat:
    test_stat=args.test_stat
else:
    #print "default stat test :: Chi2Test"
    print "default stat test :: Chi2Test,KolmogorovTest"
    test_stat='both'
    ##https://root.cern.ch/doc/master/classTH1.html#a6c281eebc0c0a848e7a0d620425090a5
if args.pvalue_threshold:
    pvalue_threshold=args.pvalue_threshold
else:
    print "p-value threshold -->0.00001"
    pvalue_threshold=0.00001

import ROOT
import os
#CompareHistos.py

CMSSW_BASE = os.getenv('CMSSW_BASE')

import sys
sys.path.append(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/')
from CompareHistos import CompareTGraphAsymmErrorsWithStat



#CompareTGraphAsymmErrorsWithStat("dimuon_mass",'LHAPDF306000', h1, h1stat,"MG5 v260",ROOT.kRed,h2,h2stat,"MG5 v261",ROOT.kBlue,True)

f_userconfig=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/user_config.py')
exec(f_userconfig)
f_userconfig.close()


#def CompareTGraphAsymmErrorsWithStat(xaxis,title,h1,h1stat,label1,color1,h2,h2stat,label2,color2,store_file_path,do_norm=False):


#f_HistoConfigForReweight=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/HistoConfigForReweight.py')
#exec(f_HistoConfigForReweight)
#f_HistoConfigForReweight.close()


f_PlotConfigForReweight=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/PlotConfigForReweight.py')
exec(f_PlotConfigForReweight)
f_PlotConfigForReweight.close()


ROOT.gROOT.LoadMacro(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/GetHisto.C')



print "===[mkComparisonPlots.py]===" 
print "[numerator] config="+nume_config+' proc='+nume_proc
print "[denominator] config="+deno_config+' proc='+deno_proc
print "[Draw]"+x +'[variation]'+variation





unit=''
if 'pt' in x or 'mass' in x: unit=' [GeV]'
                    
file0=rwgt_info[deno_config]['process'][deno_proc]['histo_path'].replace('/histoset.root','/combined_histo/combined_histo__'+variation+'__'+x+'.root'    )
file0_stat=rwgt_info[deno_config]['process'][deno_proc]['histo_path'].replace('/histoset.root','/combined_histo/combined_histo__'+variation+'__'+x+'__statonly.root'    )
file1=rwgt_info[nume_config]['process'][nume_proc]['histo_path'].replace('/histoset.root','/combined_histo/combined_histo__'+variation+'__'+x+'.root'    )
file1_stat=rwgt_info[nume_config]['process'][nume_proc]['histo_path'].replace('/histoset.root','/combined_histo/combined_histo__'+variation+'__'+x+'__statonly.root'    )

store_dir=MYWORKDIR+'/ComparisonPlots/'+dirname+'/'+variation+'/'
os.system('mkdir -p '+store_dir)
store_filepath=store_dir+'/'+x

xaxis=x+unit
#title=proc+'__'+rwgt_info[deno]['variation'][variation]['name']
#title=args.title


h0=ROOT.GetTGraphAsymmErrors(file0,'Graph')
h0stat=ROOT.GetTGraphAsymmErrors(file0_stat,'Graph')
label0=deno_alias
color0=rwgt_info[deno_config]['color']

h1=ROOT.GetTGraphAsymmErrors(file1,'Graph')
h1stat=ROOT.GetTGraphAsymmErrors(file1_stat,'Graph')
label1=nume_alias
color1=rwgt_info[nume_config]['color']

if color0==color1:
    color0=ROOT.kBlue
    color1=ROOT.kRed

CompareTGraphAsymmErrorsWithStat(xaxis,yaxis,yaxis_ratio,title,h1,h1stat,label1,color1,h0,h0stat,label0,color0,store_filepath,test_stat,pvalue_threshold,True)


del color1
del h1
del h1stat
del h0
del h0stat
