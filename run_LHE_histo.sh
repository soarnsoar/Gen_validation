


DIRLIST=()
ISTART=()
IEND=()
DIRLIST+=('JOB_mg232_dytautau012j_5f_NLO')
ISTART+=(2001)
IEND+=(2102)

ITAGMAX=`echo "scale=0; ${#DIRLIST[@]} -1 " | bc`


for ITAG in `seq 0 ${ITAGMAX}`; do
    
echo "ITAG="$ITAG
DIR=${DIRLIST[${ITAG}]}
istart=${ISTART[$ITAG]}
iend=${IEND[$ITAG]}

FILELIST=($(ls $DIR/OUTPUT_inLHE*.root))

PYTHON=run_${DIR}.py

echo "import FWCore.ParameterSet.Config as cms" > $PYTHON
echo 'process = cms.Process("Demo")' >> $PYTHON
echo 'process.load("FWCore.MessageService.MessageLogger_cfi")' >> $PYTHON
echo 'process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )'>>$PYTHON
echo 'process.TFileService = cms.Service("TFileService",'>>$PYTHON
echo 'fileName = cms.string("test_output.root"),' >> $PYTHON
echo 'closeFileFast = cms.untracked.bool(True)'>>$PYTHON
echo '                                   )' >> $PYTHON
echo 'process.source = cms.Source("PoolSource",'>>$PYTHON
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

#cmsRun $PYTHON

done