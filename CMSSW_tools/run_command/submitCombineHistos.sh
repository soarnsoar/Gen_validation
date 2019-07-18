##---Combine systematic error sets

CombineHistos.py --conf mg260LO --b &
CombineHistos.py --conf mg261LO --b &
CombineHistos.py --conf mg265LO --b &

CombineHistos.py --conf mg260NLO --b &
CombineHistos.py --conf mg261NLO --b &
CombineHistos.py --conf mg265NLO --b &

top

#CombineHistos.py --conf mg260NLO_1 --b
#CombineHistos.py --conf mg260NLO_2 --b
