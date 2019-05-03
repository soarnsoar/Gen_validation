#http://home.thep.lu.se/~torbjorn/talks/fnal04lha.pdf
##http://lcgapp.cern.ch/project/docs/lhef5.pdf
#jhchoi@cern.ch


import copy



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
        
                    thisevent.NUP=info[0]
                    Nparticle=thisevent.NUP
                    thisevent.IDPRUP=info[1]
                    thisevent.XWGTUP=info[2]
                    thisevent.SCALUP=info[3]
                    thisevent.AQEDUP=info[4]
                    thisevent.AQCDUP=info[5]
                    #print "@thisevent.NUP in info box="+str(thisevent.NUP)
                    iline+=1
                else:
                    #print "Particle info"
                    #print str(line)
                    info=line.split()
                    
                    thisptl=particle()
                    thisptl.IDUP=info[0]
                    thisptl.ISTUP=info[1]
                    thisptl.MOTHUP1=info[2]
                    thisptl.MOTHUP2=info[3]
                    thisptl.ICOLUP1=info[4]
                    thisptl.ICOLUP2=info[5]
                    thisptl.PUP1=info[6]
                    thisptl.PUP2=info[7]
                    thisptl.PUP3=info[8]
                    thisptl.PUP4=info[9]
                    thisptl.PUP5=info[10]
                    thisptl.VTIMUP=info[11]
                    thisptl.SPINUP=info[12]
                    #print "thisptl.IDUP="+str(thisptl.IDUP)
                    iline+=1
                    
                    thisevent.PARTICLE_LIST.append(copy.deepcopy(thisptl))
                    #print "@thisevent.NUP in ptl box="+str(thisevent.NUP)
                    #print "@thisevent.PARTICLE_LIST[0].IDUP in ptl box = "+str(thisevent.PARTICLE_LIST[0].IDUP)
         


def check_MH(my_event):
    MH_list=[]
    for ptl in evt.PARTICLE_LIST:
        pid=ptl.IDUP
        if pid == 25 : ##Higgs boson
            MH_list.append(ptl.PUP5)
            
    return MH_list        
           
if __name__=="__main__":
    analyzer=parser("cmsgrid_final.lhe")
    analyzer.parse_file()
    events = analyzer.EVENT_LIST
    for evt in events:
        print "------"+str(events.index(evt))+"-----"
        #for ptl in evt.PARTICLE_LIST:
            #print "idx="+str(evt.PARTICLE_LIST.index(ptl))+"pid="+str(ptl.IDUP)+" status="+str(ptl.ISTUP)


