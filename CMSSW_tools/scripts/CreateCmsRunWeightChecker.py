#!/usr/bin/env python                                                                                                                                                             

import os
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--rootfile", help="input root file path")

args = parser.parse_args()

if args.rootfile:
    rootfile=args.rootfile
else:
    print "need --rootfile option"
    exit()


def CreateConfigPy(rootfile):
    
    
    
    fnew=open('RunWeightChecker.py','w')
    print >>fnew,'''
import FWCore.ParameterSet.Config as cms

process = cms.Process("DYValidation")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )



process.source = cms.Source("PoolSource",
                                    # replace 'myfile.root' with the source file you want to use
           fileNames = cms.untracked.vstring(


"{0}"
      )
)

process.DYValidation = cms.EDAnalyzer('weight_checker',

                              genSrc = cms.InputTag("genParticles")
#prunedGenParticles
)


process.p = cms.Path(process.DYValidation)
        '''.format(rootfile)
        
    fnew.close()





if __name__ == "__main__":

    ##Load HistoConfig##
    CreateConfigPy(rootfile)
    

    ##HistoConfig['varname']
    ##HistoConfig['title']
    ##HistoConfig['nbin']
    ##HistoConfig['xmin']
    ##HistoConfig['xmax']
    




