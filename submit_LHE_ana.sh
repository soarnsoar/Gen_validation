#!/bin/bash
##This is for KISTI job
function run_template(){

echo '#!/bin/bash' > run_template.sh                           
echo 'SECTION=`printf %03d $1`' >> run_template.sh
echo 'WORKDIR=`pwd`'>> run_template.sh
echo 'echo "#### Extracting cmssw ####"'>> run_template.sh
echo 'tar -zxf INPUT.tar.gz'>> run_template.sh
echo 'echo "#### cmsenv ####"'>> run_template.sh
echo 'export CMS_PATH=/cvmfs/cms.cern.ch'>> run_template.sh
echo 'source $CMS_PATH/cmsset_default.sh'>> run_template.sh
echo 'export SCRAM_ARCH=slc6_amd64_gcc630'>> run_template.sh

echo 'cd CMSSW_9_3_8/src'>> run_template.sh
echo 'scram build ProjectRename'>> run_template.sh
echo 'eval `scramv1 runtime -sh`'>> run_template.sh
echo 'cd ../../'>> run_template.sh
echo 'cmsRun __SCRIPT__.py'>> run_template.sh

}
CURDIR=`pwd`
function batch_creater(){
    echo "===batch_creater_jhchoi.sh==="
#############Set variable##########
    #CURDIR=`pwd`
    
    JOBNAME="TREEJOB_"$1
    NJOBS=$2
    PYTHON=$3
    echo "JOB DIR ="$JOBNAME
##input tar's name => INPUT.tar.gz
    
###################################
    
    
    if [ -z $2 ];then
	echo "default NJOBs = 1"
	NJOBS=1
    fi
    
    
    
    
    
#########Check input argument######
    if [ -z $1 ];then
	echo "Need argument"
	
	
#########Check alreay job env######
    elif [ -d $JOBNAME ];then
	echo "The job directory alreay exists"
	
    else
	
##Make tar input
	
#tar -cvzf INPUT.tar.gz *
	echo "===Make INPUT.tar.gz==="
	
	
	tar -czf INPUT_${1}.tar.gz CMSSW* $PYTHON.py
	
#$JOBNAME
	
	mkdir $JOBNAME
	pushd $JOBNAME
	mv ../INPUT_${1}.tar.gz INPUT.tar.gz
	
	echo "===Make submit.jds==="
	
	echo "executable = run_${1}.sh" > submit.jds 
	echo "universe   = vanilla" >> submit.jds
	echo "arguments  = \$(Process)" >> submit.jds
	
	
	if [[ "$HOSTNAME" =~ "sdfarm" ]];then
	    echo 'requirements = ( HasSingularity == true )' >> submit.jds
	    echo 'accounting_group = group_cms' >> submit.jds
	    echo '+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest"' >> submit.jds
	    echo '+SingularityBind = "/cvmfs, /cms, /share"' >> submit.jds
	elif [[ "$HOSTNAME" =~ "lxplus" ]];then
	    echo '+JobFlavour = "longlunch"' >> submit.jds
	fi
	echo "log = condor.log" >> submit.jds
	echo "getenv     = True" >> submit.jds
	echo "should_transfer_files = YES" >> submit.jds
	echo "when_to_transfer_output = ON_EXIT" >> submit.jds
	echo "output = job_\$(Process).log" >> submit.jds
	echo "error = job_\$(Process).err" >> submit.jds
	echo "transfer_input_files = INPUT.tar.gz" >> submit.jds
	echo "transfer_output_files = Evt_Tree.root" >> submit.jds
	echo "queue $NJOBS" >> submit.jds
	
	
	echo "===Make submit.jds DONE.==="
	
    fi
###################################
    
    #cd $CURDIR
    popd
##then move to $JOBNAME directory and
##make run.sh script
##make output file name to OUTPUT.root
#condor_submit submit.jds
    
    
    echo "batch_creater_jhchoi.sh DONE."
    
}

function submit_batch(){
    #OTAG=$1
    JOB=$1
    PYTHON=$2
    
    batch_creater $JOB 1 $PYTHON
    pushd TREEJOB_$JOB
    cp ../run_template.sh run_$JOB.sh


    
    find . -name run_$JOB.sh | xargs perl -pi -e s/__SCRIPT__/$PYTHON/g
    #find . -name run_$JOB.sh | xargs perl -pi -e s/__INPUT_EDM__/"$INPUTEDM"/g
    
    condor_submit submit.jds &> submit_id.txt
    cat submit_id.txt
    popd
}


##This is main###
### settings to modify
# specify batch system 

# number of jobs 
NFILE=100
# number of events per job 
WORKDIR=`pwd -P`
# path for private fragments not yet in cmssw
OTAGLIST=()
export SCRAM_ARCH=slc6_amd64_gcc630
#SCRAM_ARCH=slc6_amd64_gcc481
RELEASE=CMSSW_9_3_8
#RELEASE=CMSSW_7_1_30

OTAGLIST+=(mg260_dytautau012j_5f_NLO)
OTAGLIST+=(mg232_dytautau012j_5f_NLO)
#OTAGLIST+=(mg242_dyellell012j_5f_NLO_tautau_filter)

#GRIDPACKLIST+=( ${WORKDIR}/dyellell01234j_5f_LO_MLM_VMG5_26x_false_pdfwgt_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz ${WORKDIR}/dyellell


### start tag loop for setups to be validated  
NTAG=`echo "scale=0; ${#OTAGLIST[@]} -1 " | bc` 

for ITAG in `seq 0 ${NTAG}`; do
    OTAG=${OTAGLIST[${ITAG}]}
    echo "OTAG="$OTAG
    ### move to submission directory 
    cd ${WORKDIR}
    FMAX=`expr $NFILE - 1`
    for FTAG in `seq 0 ${FMAX}`; do
	
	echo "OTAG="$OTAG
    ### prepare submission script 
	echo "FTAG="$FTAG
	#OUTPUT_inLHE_54
	F_INPUT=`ls ${CURDIR}/JOB_$OTAG/OUTPUT_inLHE_${FTAG}.root`

	
	echo 'import FWCore.ParameterSet.Config as cms' > TreeRun_${OTAG}_${FTAG}.py
	echo 'process = cms.Process("Demo")' >> TreeRun_${OTAG}_${FTAG}.py
	echo 'process.load("FWCore.MessageService.MessageLogger_cfi")' >> TreeRun_${OTAG}_${FTAG}.py
	echo 'process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )' >> TreeRun_${OTAG}_${FTAG}.py
	echo 'process.TFileService = cms.Service("TFileService",' >> TreeRun_${OTAG}_${FTAG}.py
	echo 'fileName = cms.string("Evt_Tree.root"),'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'closeFileFast = cms.untracked.bool(True)'>>TreeRun_${OTAG}_${FTAG}.py
	echo ')'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'process.source = cms.Source("PoolSource",'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'fileNames = cms.untracked.vstring('>>TreeRun_${OTAG}_${FTAG}.py
	echo '"file:'"${F_INPUT}"'"))'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'process.demo = cms.EDAnalyzer("JHanalyzer_tautau_inLHE",'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'genSrc = cms.InputTag("genParticles"))'>>TreeRun_${OTAG}_${FTAG}.py
	echo 'process.p = cms.Path(process.demo)'>>TreeRun_${OTAG}_${FTAG}.py
	
#    cp ${CMSSW_BASE}/src/Configuration/Generator/python/TreeRun_${OTAG}_${FTAG}.py . 
	
### adjust random numbers 
	
	run_template
	echo "OTAG_FTAG="${OTAG}_${FTAG}
	submit_batch ${OTAG}_${FTAG} TreeRun_${OTAG}_${FTAG}
    done
done # end of tag loop 






