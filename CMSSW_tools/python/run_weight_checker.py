import FWCore.ParameterSet.Config as cms

process = cms.Process("DYValidation")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )


        
process.source = cms.Source("PoolSource",
                                    # replace 'myfile.root' with the source file you want to use                                                                      
           fileNames = cms.untracked.vstring(



#"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg260_master_dyellell01234j_5f_LO_MLM__5000evt/OUTPUT_0.root",\
#"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg261_dyellell01234j_5f_LO_MLM__5000evt/OUTPUT_0.root",\
#"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg265_dyellell01234j_5f_LO_MLM__5000evt/OUTPUT_0.root",\
#"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg260_master_dyellell012j_5f_NLO_FXFX__5000evt/OUTPUT_0.root",\
#"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg261_dyellell012j_5f_NLO_FXFX__5000evt/OUTPUT_0.root" ,\
"file:/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR__GENEVT_mg265_dyellell012j_5f_NLO_FXFX__5000evt/OUTPUT_0.root" ,\




     )
)
       
process.DYValidation = cms.EDAnalyzer('weight_checker',
                              
                              genSrc = cms.InputTag("genParticles")
#prunedGenParticles
)


process.p = cms.Path(process.DYValidation)
