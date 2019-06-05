EXT="tar.xz"
LHENAME='cmsgrid_final.lhe'  
process=$1

ARR_TAR=( $(ls ${process}"_slc*.${EXT}") )


for gridpack in ${ARR_TAR[@]};do


    echo "@@TEST "${gridpack}"@@"
    TESTDIR=test_${gridpack%".${EXT}"}
    if [ -d $TESTDIR ];then
	echo "Already exists ""$TESTDIR"
	continue
    fi
    mkdir -p ${TESTDIR}
    pushd $TESTDIR
    tar -xf ../${gridpack}
    ./runcmsgrid.sh 10 10 10 &> test_log.txt
    
    SUCCESS=0
    if [ -f "$LHENAME" ];then
	
	#echo "!!"
	SUCCESS=1
    fi
    
    popd
    
    
    if [ $SUCCESS -eq 1 ];then
	
	echo -e "${gridpack}\nDIR=$PWD\n[DONE]\n" | /bin/mailx -s '[DONE]Gridpack ST_TEST ${gridpack}' soarnsoar@gmail.com
	
    else
	
	echo -e "${gridpack}\nDIR=$PWD\n[FAIL]\n" | /bin/mailx -s '[FAIL]Gridpack ST_TEST ${gridpack}' soarnsoar@gmail.com
	
	
    fi
    
    
done
