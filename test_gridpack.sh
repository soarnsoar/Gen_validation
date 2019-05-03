EXT="tar.xz"
ARR_TAR=( $(ls *".${EXT}") )


for gridpack in ${ARR_TAR[@]};do
    echo "@@TEST "${gridpack}"@@"
    TESTDIR=test_${gridpack%".${EXT}"}
    mkdir -p ${TESTDIR}
    pushd $TESTDIR
    tar -xf ../${gridpack}
    ./runcmsgrid.sh 10 10 10 &> test_log.txt &
    popd

    
done
