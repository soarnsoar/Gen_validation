import FWCore.ParameterSet.Config as cms

process = cms.Process("DYValidation")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.TFileService = cms.Service("TFileService",                                                                                                                               
                                   fileName = cms.string("test.root"),
                                   closeFileFast = cms.untracked.bool(True)
                               )                                                                                                                                             


        
process.source = cms.Source("PoolSource",
                                    # replace 'myfile.root' with the source file you want to use                                                                      
           fileNames = cms.untracked.vstring(


"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/test_file/mg260_master_dyellell012j_5f_NLO_FXFX__5000evt.root"
      )
)
       
process.DYValidation = cms.EDAnalyzer('HistoFactoryDYKinematics',
                              
                              genSrc = cms.InputTag("genParticles")
#prunedGenParticles
)


process.p = cms.Path(process.DYValidation)
