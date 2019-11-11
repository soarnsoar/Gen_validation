gridpack=$1


echo "@@TEST "${gridpack}"@@"
TESTDIR=test_${gridpack%".${EXT}"}
if [ -d $TESTDIR ];then
    echo "Already exists ""$TESTDIR"
    continue
fi
mkdir -p ${TESTDIR}
pushd $TESTDIR
tar -xf ../${gridpack}
./runcmsgrid.sh 10 10 10 &> test_log.txt &
popd

    

