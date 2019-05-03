ARR_JOBDIR=($(ls -d JOB*))
for jobdir in ${ARR_JOBDIR[@]};do
    echo "-----------$jobdir-----------"
    pushd $jobdir

    ARR_ERRFILE=($(ls *.err))



    mkdir -p trash
    NTOTAL=0
    NFAIL=0
    NSUCCESS=0
    for errfile in ${ARR_ERRFILE[@]};do
	echo "@${errfile}@"
	Errno=`cat ${errfile} | grep Errno`
	error=`cat ${errfile} | grep error`
	num=${errfile%".err"}
	num=${num#"job_"}
	if [ -n "$Errno" ];then
	    echo "@@Errno detected@@"
	    mv OUTPUT_${num}.root trash/
	    NFAIL=`expr $NFAIL + 1`
	elif [ -n "$error" ];then
	    echo "@@error detected@@"
	    mv OUTPUT_${num}.root trash/
	    NFAIL=`expr $NFAIL + 1`
	else
	    NSUCCESS=`expr $NSUCCESS + 1`
	fi
	
	
    done
 

    popd
    echo "---summary---"
    echo "NTOTAL="$NTOTAL
    echo "NSUCCESS="$NSUCCESS
    echo "NFAIL="$NFAIL
    
    echo "NTOTAL="$NTOTAL > summary_${jobdir}.txt
    echo "NSUCCESS="$NSUCCESS >> summary_${jobdir}.txt
    echo "NFAIL="$NFAIL >> summary_${jobdir}.txt

done
