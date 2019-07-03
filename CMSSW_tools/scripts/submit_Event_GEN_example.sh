ARR_VMG=()
ARR_VMG+=(mg260_master)
ARR_VMG+=(mg261)
ARR_VMG+=(mg265)


NEVENT=5000
i_seed=0
f_seed=49
for vmg in ${ARR_VMG[@]};do

    mkGENevt.py --fragment /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/fragments/Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_qCut19_LHE_pythia8_cff.py --nevent ${NEVENT} --startseed ${i_seed} --endseed ${f_seed} --tag GENEVT_${vmg}_dyellell01234j_5f_LO_MLM --gridpack /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/gridpacks/cms1/${vmg}/dyellell01234j_5f_LO_MLM_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz


    mkGENevt.py --fragment /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/fragments/Hadronizer_TuneCP5_13TeV_aMCatNLO_FXFX_5f_max2j_LHE_pythia8_cff.py --nevent ${NEVENT} --startseed ${i_seed} --endseed ${f_seed} --tag GENEVT_${vmg}_dyellell012j_5f_NLO_FXFX --gridpack /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/gridpacks/cms1/${vmg}/dyellell012j_5f_NLO_FXFX_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz


done

#mkGENevt.py --fragment /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/fragments/Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_qCut19_LHE_pythia8_cff.py --nevent 5000 --startseed 1 --endseed 200 --tag GENEVT_mg261_dyellell01234j_5f_LO_MLM --gridpack /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/gridpacks/cms1/mg261/dyellell01234j_5f_LO_MLM_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz


#mkGENevt.py --fragment /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/fragments/Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_qCut19_LHE_pythia8_cff.py --nevent 5000 --startseed 1 --endseed 200 --tag GENEVT_mg265_dyellell01234j_5f_LO_MLM --gridpack /cms/ldap_home/jhchoi/gridvalidation/mg265_validation/gridpacks/cms1/mg265/dyellell01234j_5f_LO_MLM_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz
