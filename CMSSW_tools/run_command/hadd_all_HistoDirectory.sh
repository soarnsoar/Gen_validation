ARR_DIR=($(ls -d JOBDIR_HistoFactory*/))

for dir in ${ARR_DIR[@]};do
    python hadd_500.py --directory ${dir} &
done
