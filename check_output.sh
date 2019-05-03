ARR_JOBDIR=($(ls -d JOB*))
for jobdir in ${ARR_JOBDIR[@]};do
    echo "-----------$jobdir-----------"
    pushd $jobdir

    ARR_ERRFILE=($(ls *.err))



    mkdir -p trash
    for errfile in ${ARR_ERRFILE[@]};do
	echo "@${errfile}@"
	Errno=`cat ${errfile} | grep Errno`
	error=`cat ${errfile} | grep error`
	num=${errfile%".err"}
	num=${num#"job_"}
	if [ -n "$Errno" ];then
	    echo "@@Errno detected@@"
	    mv OUTPUT_${num}.root trash/
	elif [ -n "$error" ];then
	    echo "@@error detected@@"
	    mv OUTPUT_${num}.root trash/
	fi
	
	
    done
 

    popd
done