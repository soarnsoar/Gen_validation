import ROOT
import os
import copy

#--Set CMSSW_BASE path
CMSSW_BASE = os.getenv('CMSSW_BASE')

#--Set modules path
import sys
sys.path.append(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules')

from GetCombinedHisto import GetCombinedHisto 

##--No Graphical Window

ROOT.gROOT.SetBatch(ROOT.kTRUE)


##--Configration

f=open(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/PlotConfigForReweight.py','r')

exec(f)


ROOT.gROOT.LoadMacro(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/GetHisto.C')
#rwgt_info['mg260LO']
#rwgt_info['mg261LO']
#rwgt_info['mg265LO']

#rwgt_info['mg260NLO']
#rwgt_info['mg261NLO']
#rwgt_info['mg265NLO']

#variations=['muRmuF','306000','322500','322700','322900','323100','323300','323500','323700','323900','305800','13000','13065','13069','13100','13163','13167','13200','25200','25300','25000','42780','90200','91200','90400','91400','61100','61130','61100','61230','13400','82200','292200',]

LOconfigs=['mg260LO','mg261LO','mg265LO']
#LOprocesses=['dyellell01234j_5f_LO_MLM','dyellell01234j_5f_LO_MLM_pdfwgt_T']
for config in LOconfigs:
    this_rwgt_info=rwgt_info[config]
    for proc in this_rwgt_info['process']:
        histopath=this_rwgt_info['process'][proc]
        for var in this_rwgt_info['variation']:
            
            combination=this_rwgt_info['variation'][var]['combination']
            name=this_rwgt_info['variation'][var]['name']
            idx_list=this_rwgt_info['variation'][var]['idx']
            for x in xname:
                ##x = variable name such as Zmuon_pt
                hlist=[]
                for idx in idx_list:
                    h=ROOT.GetHisto(histopath,"DYValidation/"+x+'_'+str(idx))
                    hlist.append(copy.deepcopy(h))
                h_combined=GetCombinedHisto(test_hlist,combination,name)
                del hlist


tcanvas =ROOT.TCanvas( "cc", "cc" , 800, 600 )
h_combined.Draw()
tcanvas.SaveAs('a.png')
#tcanvas =ROOT.TCanvas( "cc", "cc" , 800, 600 )
#h.Draw()
#tcanvas.SaveAs('a.png')
##Draw variable
#TGraphAsymmErrors
#ROOT.TGraphAsymmErrors()
#fileIn=ROOT.TFile.Open("/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell01234j_5f_LO_MLM__5000evt/combined_histo.root"
