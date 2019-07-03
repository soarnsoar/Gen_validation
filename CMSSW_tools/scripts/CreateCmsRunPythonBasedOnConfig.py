#!/usr/bin/env python                                                                                                                                                             

import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="config file path")
parser.add_argument("--rootfile", help="input root file path")

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


def CreateConfigPy(HistoConfig,rootfile):
    ccname='HistoFactoryDYKinematics'
    
    for key in HistoConfig:
        
        #title=HistoConfig[key]['title']
        #nbin=str(HistoConfig[key]['nbin'])
        #xmin=str(HistoConfig[key]['xmin'])
        #xmax=str(HistoConfig[key]['xmax'])
        #varname=HistoConfig[key]['varname']
        
        ccToRun=ccname+'__'+key+'__'
    
        fnew=open('RunHistoFactory__'+key+'__.py','w')
        print >>fnew,'''
import FWCore.ParameterSet.Config as cms
process = cms.Process("DYValidation")
process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("HISTO__{0}__.root"),
                                   closeFileFast = cms.untracked.bool(True)
                               )



process.source = cms.Source("PoolSource",
                                    # replace 'myfile.root' with the source file you want to use
           fileNames = cms.untracked.vstring(


"{1}"
      )
)

process.DYValidation = cms.EDAnalyzer('HistoFactoryDYKinematics__{2}__',

                              genSrc = cms.InputTag("genParticles")
#prunedGenParticles
)


process.p = cms.Path(process.DYValidation)
        '''.format(key,rootfile,key)
        
        fnew.close()





if __name__ == "__main__":

    ##Load HistoConfig##
    f=open(config)
    exec(f)
    f.close()
    
    CreateConfigPy(HistoConfig,rootfile)
    

    ##HistoConfig['varname']
    ##HistoConfig['title']
    ##HistoConfig['nbin']
    ##HistoConfig['xmin']
    ##HistoConfig['xmax']
    




