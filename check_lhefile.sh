ARR_TESTDIR=($(ls -d test_*/))

for testdir in ${ARR_TESTDIR[@]};do
    echo "@@${testdir}@@@"
    if [ -f $testdir/cmsgrid_final.lhe ];then
	echo checked
    else
	echo "!!!!!!!!!!NO LHE!!!!!!!!!"
    fi

done
