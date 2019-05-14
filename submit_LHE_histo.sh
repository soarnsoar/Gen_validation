CURDIR=`pwd`
PREFIX=HISTOJOB
############
RELEASE=CMSSW_9_3_8
scram_arch=slc6_amd64_gcc630
#############

###function for batch###
function run_template(){

RUNPY=$1

echo '#!/bin/bash' > run_template.sh
echo 'SECTION=`printf %03d $1`' >> run_template.sh
echo 'WORKDIR=`pwd`'>> run_template.sh
echo 'echo "#### Extracting cmssw ####"'>> run_template.sh
echo 'tar -zxf INPUT.tar.gz'>> run_template.sh
echo 'echo "#### cmsenv ####"'>> run_template.sh
echo 'export CMS_PATH=/cvmfs/cms.cern.ch'>> run_template.sh
echo 'source $CMS_PATH/cmsset_default.sh'>> run_template.sh
echo 'export SCRAM_ARCH='$scram_arch>> run_template.sh

echo 'cd '$RELEASE'/src'>> run_template.sh
echo 'scram build ProjectRename'>> run_template.sh
echo 'eval `scramv1 runtime -sh`'>> run_template.sh
echo 'cd ../../'>> run_template.sh
echo 'cmsRun '$RUNPY >> run_template.sh

}
###

function submit_batch(){
    JOB=$1
    PYTHON=$2
    
    batch_creater $JOB 1 $PYTHON
    pushd ${PREFIX}_$JOB
    cp ../run_template.sh run_$JOB.sh

    find . -name run_$JOB.sh | xargs perl -pi -e s/__SCRIPT__/$PYTHON/g

    condor_submit submit.jds &> submit_id.txt
    cat submit_id.txt
    popd
}




#############

function batch_creater(){
    echo "===batch_creater_jhchoi.sh==="
#############Set variable##########                                                                                                         
    JOBNAME="${PREFIX}_"$1
    NJOBS=$2
    PYTHON=$3
    echo "JOB DIR ="$JOBNAME
##input tar's name => INPUT.tar.gz                                                                                                           
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

        tar -czf INPUT_${1}.tar.gz CMSSW* $PYTHON
#$JOBNAME  
        rm $PYTHON
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
        echo "transfer_output_files = output.root" >> submit.jds
        echo "queue $NJOBS" >> submit.jds


        echo "===Make submit.jds DONE.==="

    fi
    
    popd
    echo "batch_creater_jhchoi.sh DONE."
    
}
###################################   
##MAIN##
DoBATCH=1

MAXFILE=1000
DIRLIST=()
ISTART=()
IEND=()
DIRLIST+=('JOB_mg232_dytautau012j_5f_NLO')
ISTART+=(2001)
IEND+=(2102 )

DIRLIST+=('JOB_mg260_dytautau012j_5f_NLO')
ISTART+=(1974)
IEND+=(2075)
ITAGMAX=`echo "scale=0; ${#DIRLIST[@]} -1 " | bc`


for ITAG in `seq 0 ${ITAGMAX}`; do
    
echo "ITAG="$ITAG
DIR=${DIRLIST[${ITAG}]}
istart=${ISTART[$ITAG]}
iend=${IEND[$ITAG]}

FILELIST=($(ls ${CURDIR}/$DIR/OUTPUT_inLHE*.root))

PYTHON=run_${DIR}.py

echo "import FWCore.ParameterSet.Config as cms" > $PYTHON
echo 'process = cms.Process("Demo")' >> $PYTHON
echo 'process.load("FWCore.MessageService.MessageLogger_cfi")' >> $PYTHON
echo 'process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )'>>$PYTHON
echo 'process.TFileService = cms.Service("TFileService",'>>$PYTHON
echo 'fileName = cms.string("'${DIR}'_output.root"),' >> $PYTHON
#echo 'closeFileFast = cms.untracked.bool(True)'>>$PYTHON
echo '                                   )' >> $PYTHON
echo 'process.source = cms.Source("PoolSource",'>>$PYTHON
echo ' duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),' >> $PYTHON
echo 'fileNames = cms.untracked.vstring('>>$PYTHON

for FILE in ${FILELIST[@]};do
    echo '"file:'$FILE'",'>>$PYTHON
done
echo '      )' >> $PYTHON
echo ')' >> $PYTHON
echo 'process.demo = cms.EDAnalyzer("JHanalyzer_tautau_inLHE",'>>$PYTHON
echo 'genSrc = cms.InputTag("genParticles"),'>>$PYTHON
echo "istart=cms.uint32(${istart})," >> $PYTHON
echo "iend=cms.uint32($iend)," >> $PYTHON
echo ')'>>$PYTHON
echo 'process.p = cms.Path(process.demo)'>>$PYTHON

if [ $DoBATCH == 0 ];then
    echo "@@NOTBATCH@@"
    cmsRun $PYTHON &> $PYTHON.log &
else
    echo "@@DOBATCH@@"
    ###Make python for each file###
    IFILEMAX=`echo "scale=0; ${#FILELIST[@]} -1 " | bc`
    
    for IFILE in `seq 0 ${IFILEMAX}`; do
	if [ $IFILE -gt $MAXFILE ];then
	    continue
	fi
	PYTHON=run_${DIR}_${IFILE}.py
	echo "import FWCore.ParameterSet.Config as cms" > $PYTHON
	echo 'process = cms.Process("Demo")' >> $PYTHON
	echo 'process.load("FWCore.MessageService.MessageLogger_cfi")' >> $PYTHON
	echo 'process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )'>>$PYTHON
	echo 'process.TFileService = cms.Service("TFileService",'>>$PYTHON
	echo 'fileName = cms.string("output.root"),' >> $PYTHON
	echo '                                   )' >> $PYTHON
	echo 'process.source = cms.Source("PoolSource",'>>$PYTHON
	echo ' duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),' >> $PYTHON
	echo 'fileNames = cms.untracked.vstring('>>$PYTHON
	FILE=${FILELIST[${IFILE}]}
	echo '"file:'$FILE'",'>>$PYTHON
	echo '      )' >> $PYTHON
	echo ')' >> $PYTHON
	echo 'process.demo = cms.EDAnalyzer("JHanalyzer_tautau_inLHE",'>>$PYTHON
	echo 'genSrc = cms.InputTag("genParticles"),'>>$PYTHON
	echo "istart=cms.uint32(${istart})," >> $PYTHON
	echo "iend=cms.uint32($iend)," >> $PYTHON
	echo ')'>>$PYTHON
	echo 'process.p = cms.Path(process.demo)'>>$PYTHON
	run_template $PYTHON
	submit_batch ${DIR}_${IFILE} ${PYTHON}
    done
    






fi    
done