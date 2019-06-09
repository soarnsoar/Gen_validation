

#source /afs/cern.ch/user/j/jhchoi/refresh_auth/refresh_10min.sh&
#source /afs/cern.ch/user/j/jhchoi/release_10sec.sh &




#mg260
#python run_gridpack_generation.py --branch master --dirname mg260_master --proc dyellell012j_5f_NLO_FXFX
#mg261
#python run_gridpack_generation.py --branch mg261 --dirname mg261 --proc dyellell012j_5f_NLO_FXFX
#mg265

python setup_gridpack_generation.py --branch mg265 --dirname mg265 --proc dyellell0j_5f_LO_MLM


#source run__master__mg260_master__dyellell012j_5f_NLO_FXFX.sh
#source run__mg261__mg261__dyellell012j_5f_NLO_FXFX.sh
source run__mg265__mg265__dyellell0j_5f_LO_MLM.sh
