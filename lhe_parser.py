#http://home.thep.lu.se/~torbjorn/talks/fnal04lha.pdf
##http://lcgapp.cern.ch/project/docs/lhef5.pdf
#jhchoi@cern.ch


import copy
import numpy
import math
import glob

import os

class event:

    def __init__(self):
        self.NUP=0 ## NParticle                                                                                                                                                               
        self.IDPRUP=0 ##: identity of current process
        self.XWGTUP=0 #event weight 
        self.SCALUP=0 #scale Q of parton distributions etc.
        self.AQEDUP=0 #a_em used in event
        self.AQCDUP=0 #a_s used in event
        self.PARTICLE_LIST=[]

class particle:

    def __init__(self):
        self.IDUP=0 #PDG identity code for particle i
        self.ISTUP=0 #status code -1=incoming 1=final 2 intermediate
        self.MOTHUP1=0 #position of one or two mothers
        self.MOTHUP2=0
        self.ICOLUP1=0 #color
        self.ICOLUP2=0 #
        self.PUP1=0 #PUP(j,i): (px, py, pz, E, m)
        self.PUP2=0
        self.PUP3=0
        self.PUP4=0
        self.PUP5=0
        self.VTIMUP=0 #invariant lifetime c*tau
        self.SPINUP=0 #spin (helicity) information




class parser:
    def __init__(self,input_file):

        self.input_file=input_file
        self.EVENT_LIST=[]
    def parse_file(self):

        f = open(self.input_file, 'r')
        lines=f.readlines()
    

        isevent=0
        #idx_evt=0
        iline=0
        thisevent=event()
        Nparticle=0
        for line in lines:
            
            #####Event block?#####
            if "<event>" in line:
                isevent=1
                continue

            elif "</event>" in line:
                isevent=0
                iline=0
                Nparticle=0
                continue
            ######################

            ###If the line is event info###
            if isevent==1:
                
                if int(iline) > int(Nparticle):
                    ## out of range
                    #print "@thisevent.NUP in out of range box="+str(thisevent.NUP)
                    isevent=0
                    thisevent.PARTICLE_LIST=copy.deepcopy(thisevent.PARTICLE_LIST)
                    #print str(thisevent.PARTICLE_LIST[0].IDUP)
                    self.EVENT_LIST.append( copy.deepcopy(thisevent) )
                    

                elif iline==0: ## first line of event -> event info
                    del thisevent
                    thisevent=event()
                    info=line.split()
        
                    thisevent.NUP=float(info[0])
                    Nparticle=thisevent.NUP
                    thisevent.IDPRUP=float(info[1])
                    thisevent.XWGTUP=float(info[2])
                    thisevent.SCALUP=float(info[3])
                    thisevent.AQEDUP=float(info[4])
                    thisevent.AQCDUP=float(info[5])
                    #print "@thisevent.NUP in info box="+str(thisevent.NUP)
                    iline+=1
                else:
                    #print "Particle info"
                    #print str(line)
                    info=line.split()
                    
                    thisptl=particle()
                    thisptl.IDUP=float(info[0])
                    thisptl.ISTUP=float(info[1])
                    thisptl.MOTHUP1=float(info[2])
                    thisptl.MOTHUP2=float(info[3])
                    thisptl.ICOLUP1=float(info[4])
                    thisptl.ICOLUP2=float(info[5])
                    thisptl.PUP1=float(info[6])
                    thisptl.PUP2=float(info[7])
                    thisptl.PUP3=float(info[8])
                    thisptl.PUP4=float(info[9])
                    thisptl.PUP5=float(info[10])
                    thisptl.VTIMUP=float(info[11])
                    thisptl.SPINUP=float(info[12])
                    #print "thisptl.IDUP="+str(thisptl.IDUP)
                    iline+=1
                    
                    thisevent.PARTICLE_LIST.append(copy.deepcopy(thisptl))
                    #print "@thisevent.NUP in ptl box="+str(thisevent.NUP)
                    #print "@thisevent.PARTICLE_LIST[0].IDUP in ptl box = "+str(thisevent.PARTICLE_LIST[0].IDUP)
         

        f.close()
def check_MH(my_event):
    MH_list=[]
    for ptl in my_event.PARTICLE_LIST:
        pid=ptl.IDUP
        #print "idx="+str(evt.PARTICLE_LIST.index(ptl))+"pid="+str(ptl.IDUP)+" status="+str(ptl.ISTUP)
        if pid == 25 : ##Higgs boson
            #print "HIGGS"
            MH_list.append(ptl.PUP5)
            
    return MH_list        


def cal_MH(my_file):
    analyzer=parser(my_file)
    analyzer.parse_file()
    events = analyzer.EVENT_LIST
    MH_list=[]
    for evt in events:
        #print "------"+str(events.index(evt))+"-----"                                                                                                                                       
        #for ptl in evt.PARTICLE_LIST:
        #print "idx="+str(evt.PARTICLE_LIST.index(ptl))+"pid="+str(ptl.IDUP)+" status="+str(ptl.ISTUP)                                                                                     
        MH_list+=check_MH(evt)

    #print MH_list
    #print "<MH>="+str(numpy.mean(MH_list))
    #print "d<MH>="+str(numpy.std(MH_list)/math.sqrt(len((MH_list))))
    dic={'MH':numpy.mean(MH_list), \
         'dMH':numpy.std(MH_list)/math.sqrt(len((MH_list))) \
     }
    return dic
def get_MH_powheg_card(cardpath):
    f = open(cardpath,'r')
    lines=f.readlines()
    hmass=0
    for line in lines: 
        line=line.lstrip()
        if len(line) == 0:
            continue

        #====MH====#
        if "hmass" in line.split()[0]:

            hmass_fort=line.split()[1]
            hmass = float(hmass_fort.replace("d","E"))
            
            break
    #print "hmass="+str(hmass)
    f.close()
    return hmass

if __name__=="__main__" :
    dirlist=glob.glob("test_*")
    #print str(dirlist)
    for mydir in dirlist:

        if not os.path.isdir(str(mydir)):
            continue
        

        #print "---"+mydir+"----"
        #os.system("cat "+mydir+"/powheg.input | grep hmass")
        MH_set=get_MH_powheg_card(mydir+"/powheg.input")
        #print_MH(mydir+"/cmsgrid_final.lhe")
        MH_cal=cal_MH(mydir+"/cmsgrid_final.lhe")
        if abs(MH_set-MH_cal["MH"]) > 2*MH_cal["dMH"]:
            print "\n"
            print "------------"
            print mydir
            print "@MH_set="+str(MH_set)
            print '@MH_cal["MH]='+str(MH_cal["MH"])
            print '@MH_cal["dMH"]='+str(MH_cal["dMH"])
    #print_HM("cmsgrid_final.lhe")
