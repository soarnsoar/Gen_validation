#!/usr/bin/env python                                                                                                                                                             

import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="config file path")
parser.add_argument("--rootfile", help="rootfile file path")

args = parser.parse_args()

if args.config:
    config=args.config
else:
    print "need --config option"
    exit()

if args.rootfile:
    rootfile=args.rootfile
else:
    print "need --rootfile option"
    exit()



def GetNweight(rootfile):
    os.system('CreateCmsRunWeightChecker.py --rootfile '+rootfile)
    os.system('cmsRun RunWeightChecker.py > WeightInfo.txt')
    f=open('WeightInfo.txt','r')
    lines=f.readlines()
    Nweight=0
    for line in lines:
        if 'lheinfoweightsize=' in line.replace(' ',''):
            Nweight=int(line.replace(' ','').replace('lheinfoweightsize=',''))
    print 'Nweight='+str(Nweight)
    return Nweight


def ApplyHistoConfig(cc,HistoConfig,Nweight):

    for key in HistoConfig:


        f=open(cc,'r')
        name=cc.split(".cc")[0]
        fnew=open(name+'__'+key+'__.cc','w')
        lines=f.readlines()

        title=HistoConfig[key]['title']
        nbin=str(HistoConfig[key]['nbin'])
        xmin=str(HistoConfig[key]['xmin'])
        xmax=str(HistoConfig[key]['xmax'])
        varname=HistoConfig[key]['varname']
    
    

        for line in lines:
            if name in line:
                fnew.write(line.replace(name,name+"__"+key+'__'))
            elif '//<JHCHOI_HISTO_DEFINE>//' in line:
                for i in range(0,Nweight):
                    fnew.write('h_'+key+'_'+str(i)+'=fs->make<TH1D>("'+title+"_"+str(i)+'","'+title+'_'+str(i)+'",'+nbin+','+xmin+','+xmax+');')
                    fnew.write('\n')
            elif '//<JHCHOI_HISTO_DECLARE>//' in line:
                for i in range(0,Nweight):
                    fnew.write('TH1D *h_'+title+'_'+str(i)+';')
                    fnew.write('\n')
        
            elif '//<isDYmuonEventArea>//' in line:
                if 'muon' in key:
                    for i in range(0,Nweight):
                        fnew.write('h_'+title+'_'+str(i)+'->Fill('+varname+','+'LHEInfo->weights()['+str(i)+'].wgt/w0'+');')
                        fnew.write('\n')
            
            elif '//<isDYelectronEventArea>//' in line:
                if 'electron' in key:
                    for i in range(0,Nweight):
                        fnew.write('h_'+title+'_'+str(i)+'->Fill('+varname+','+'LHEInfo->weights()['+str(i)+'].wgt/w0'+');')
                        fnew.write('\n')

                
        

            else:fnew.write(line)
        
        f.close()
        fnew.close()





if __name__ == "__main__":

    ##Load HistoConfig##
    f=open(config)
    exec(f)
    f.close()
    cc='HistoFactoryDYKinematics.cc'

    Nweight=GetNweight(rootfile)

    ApplyHistoConfig(cc,HistoConfig,Nweight)
    

    ##HistoConfig['varname']
    ##HistoConfig['title']
    ##HistoConfig['nbin']
    ##HistoConfig['xmin']
    ##HistoConfig['xmax']
    




