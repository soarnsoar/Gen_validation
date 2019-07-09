import ROOT
import math
from array import array


##Type of systematic cal.
#https://arxiv.org/pdf/1412.7420.pdf
#symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ]
#replicas   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
#hessian   :up-element & down-element
##sigma+ = sqrt[ Sum[ max(F_i_up - F_0 , F_i_down - F_0, 0 )^2   ]   ]
##sigma- = sqrt[ Sum[ max(F_0 - F_i_up , F+0 - F_i_down, 0 )^2   ]   ]

#---Predefined functions


def SerError_envelope_iBin(hlist,iBin,evy_up,evy_dn): 
    if iBin==0 :print ">>>>[combination] envelope"
    ##evy_up , evy_dn -> mutable variable -> if chaned in a function, then the changed value will be remained after the function 
    ## Scan all histo ##                                                                                                                              

    

    ycenter=hlist[0].GetBinContent (iBin)
    ymax=ycenter
    ymin=ycenter
    for h in hlist:
    
        y_=h.GetBinContent(iBin)
        if y_ > ymax : 
            ymax = y_
        elif y_ < ymin : 
            ymin = y_



    ## Put max/min

    evy_up.append( abs(ymax - ycenter) )
    evy_dn.append( abs(ycenter-ymin)   )

    
def SetError_symmhessian_iBin(hlist,iBin,evy_up,evy_dn):
    if iBin==0 :print ">>>>[combination] SetError_symmhessian_iBin"
    #symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ]                                                                            
    ycenter=hlist[0].GetBinContent (iBin) ##F_0                                                                                                       
    Sum=0
    for h in hlist:
        y_=h.GetBinContent (iBin) ##F_i                                                                                                               
        Sum+= (ycenter-y_)**2
    sigma=math.sqrt(Sum)
    evy_up.append(sigma)
    evy_dn.append(sigma)

def SetError_symmhessian_as_iBin(hlist,iBin,evy_up,evy_dn):
    #symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ]                                                                            
    #a_s -> last two elements ->F+, F-                                                                                                                    
    # sigma_as = abs(F+ - F-) /2                                                                                                                          
    if iBin==0 :print ">>>>[combination] symmhessian+as"
    ycenter=hlist[0].GetBinContent (iBin) ##F_0                                                                                                       
    Sum=0
    for h in hlist[0:-2]:
        y_=h.GetBinContent (iBin) ##F_i                                                                                                               
        Sum+= (ycenter-y_)**2
        sigma=math.sqrt(Sum)
        
        #sigma_as                                                                                                                                         
        
    y1_ = hlist[-1].GetBinContent (iBin)
    y2_ = hlist[-2].GetBinContent (iBin)
    sigma_as= abs(y1_-y2_)/2

    sigma=math.sqrt(sigma**2 + sigma_as**2)

    evy_up.append(sigma)
    evy_dn.append(sigma)
def SetError_replicas_iBin(hlist,iBin,evy_up,evy_dn):
    if iBin==0 :print ">>>>[combination] replicas"
    ##replicas   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
    
    Sum=0
    Sum2=0 ## sum of squared values                                                                                                                   
    for h in hlist[1:]:
        y_=h.GetBinContent (iBin) ##F_i                                                                                                               
        Sum+= y_
        Sum2+=y_**2
    N_rep = float(len(hlist)-1)
    avg=Sum/N_rep
    avg_sq=Sum2/N_rep
    
    sigma= math.sqrt( N_rep/(N_rep-1) *( avg_sq - avg**2  )   )

    evy_up.append(sigma)
    evy_dn.append(sigma)


def SetError_replicas_as_iBin(hlist,iBin,evy_up,evy_dn):
    ##replicas   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
    if iBin==0 :print ">>>>[combination] replicas+as"
    
    Sum=0
    Sum2=0 ## sum of squared values                                                                                                                   
    for h in hlist[0:-2]:
        y_=h.GetBinContent (iBin) ##F_i                                                                                                               
        Sum+= y_
        Sum2+=y_**2
    N_rep=float(len(hlist)-1)
    avg=Sum/N_rep
    avg_sq=Sum2/N_rep
    
    sigma= math.sqrt( N_rep/(N_rep-1) *( avg_sq - avg**2  )   )
    
    
    
    #sigma_as                                                                                                                                         
    
    y1_ = hlist[-1].GetBinContent (iBin)
    y2_ = hlist[-2].GetBinContent (iBin)
    sigma_as= abs(y1_-y2_)/2
    
    sigma=math.sqrt(sigma**2 + sigma_as**2)
    
    evy_up.append(sigma)
    evy_dn.append(sigma)

def SetError_hessian_iBin(hlist,iBin,evy_up,evy_dn):
    if iBin==0 :print ">>>>[combination] hessian"
    #hessian   :up-element & down-element                                                                                                                 
    ##sigma+ = sqrt[ Sum[ max(F_i_up - F_0 , F_i_down - F_0, 0 )^2   ]   ]                                                                                
    ##sigma- = sqrt[ Sum[ max(F_0 - F_i_up , F+0 - F_i_down, 0 )^2   ]   ]                                                                                

    ycenter=hlist[0].GetBinContent (iBin) ##F_0                                                                                                       

    Sum1=0
    Sum2=0
    Npair=int((len(hlist)-1)/2)
    for idx in range(1,Npair+1):
        y1=hlist[2*idx].GetBinContent (iBin) ##F_i up                                                                                                 
        y2=hlist[2*idx-1].GetBinContent (iBin) ##F_i down                                                                                             
        
        Sum1+=max(y1-ycenter, y2-ycenter,0  )**2
        Sum2+=max(ycenter-y1, ycenter-y2,0  )**2
    sigma1=math.sqrt(Sum1)
    sigma2=math.sqrt(Sum2)

    evy_up.append(sigma1)
    evy_dn.append(sigma2)


def SetError_HERAPDF20_VAR_iBin(hlist,iBin,evy_up,evy_dn):
    if iBin==0 :print ">>>>[combination] custom, HERAPDF20_VAR"
    ycenter=hlist[0].GetBinContent (iBin) ##F_0                                                                                                   

    ##model error set(1-10)                                                                                                                       
    Sum1=0
    for h in hlist[1:10]:
        
        y_=h.GetBinContent (iBin)
        
        Sum1+=(ycenter-y_)**2
        sigma_model=math.sqrt(Sum1)


    ##Parametrization error set(11-13)                                                                                                            
    diff_max=0
    for h in hlist[11:13]:
        y_=h.GetBinContent (iBin)
        if abs(y_-ycenter) > diff_max : diff_max=abs(y_-ycenter)
    sigma_para=diff_max

    ## total sigma                                                                                                                                
    sigma=math.sqrt(sigma_model**2 + sigma_para**2)
    evy_up.append(sigma)
    evy_dn.append(sigma)


def SetError_CT14qed_inc_iBin(hlist,iBin,evy_up,evy_dn):
    if iBin==0 :print ">>>>[combination] custom, CT14qed_inc"
    ##Not sure this calculation is right
    ycenter=hlist[0].GetBinContent (iBin) ##F_0
    y_68 = hlist[11].GetBinContent (iBin) #p0==0.11& ->CL 68%
    sigma=abs(ycenter-y_68)
    evy_up.append(sigma)
    evy_dn.append(sigma)


#---End Predefined functions


#--Main function
def GetCombinedHisto(hlist,combination,name):
    nhist=len(hlist)
    
    if nhist==0:
        print "[GetCombinedHisto] hlist size == 0!"
        return
    
    ##--Setting bins--#
    vx=array('f')
    evx=array('f')
    vy=array('f')
    evy_dn=array('f')
    evy_up=array('f')
    estatv=array('f')
    
    ##--Central value--##
    nbin=hlist[0].GetNbinsX()
    for iBin in range(1, nbin+1):
        vx.append(  hlist[0].GetBinCenter (iBin))
        evx.append( hlist[0].GetBinWidth (iBin) / 2.)
        vy.append(  hlist[0].GetBinContent (iBin))
        estatv.append( hlist[0].GetBinError (iBin))


    ##--Set Sigma up/down
    if combination=='envelope':
        for iBin in range(1, nbin+1):
            SerError_envelope_iBin(hlist,iBin,evy_up,evy_dn)

            
    elif combination=='symmhessian':
        #symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ] 
        for iBin in range(1, nbin+1):
            SetError_symmhessian_iBin(hlist,iBin,evy_up,evy_dn)



    elif combination=='symmhessian+as':
        #symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ]
        #a_s -> last two elements ->F+, F-
        # sigma_as = abs(F+ - F-) /2
        for iBin in range(1, nbin+1):
            SetError_symmhessian_as_iBin(hlist,iBin,evy_up,evy_dn)

    

    elif combination=='replicas':
    ##replicas   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
        for iBin in range(1, nbin+1):
            SetError_replicas_iBin(hlist,iBin,evy_up,evy_dn)

    elif combination=='replicas+as':
    ##replicas   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
        for iBin in range(1, nbin+1):
            SetError_replicas_as_iBin(hlist,iBin,evy_up,evy_dn)



    elif combination=='hessian':
        #hessian   :up-element & down-element
        ##sigma+ = sqrt[ Sum[ max(F_i_up - F_0 , F_i_down - F_0, 0 )^2   ]   ]
        ##sigma- = sqrt[ Sum[ max(F_0 - F_i_up , F+0 - F_i_down, 0 )^2   ]   ]
        for iBin in range(1, nbin+1):
            ## Scan all histo ##
            SetError_hessian_iBin(hlist,iBin,evy_up,evy_dn)
    

    elif combination=='custom' or combination=='unknown':
        if name=='HERAPDF20_NLO_VAR':
            '''
    HERAPDF20 NLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all positive (negative) differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error and added in quadrature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.47,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;  mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5; mem=6 ; q2cut=5.; mem=7 ; mb=4.25;mem=8 ; mb=4.75; mem=9 ; mc=1.41;  mem=10 ; mc=1.53; mem=11 ; par2(Q0 1.6, mc1.47); mem=12 ; par3 (Q0 2.2, mc1.53); mem=13 ; par4(Duv);
            '''

            for iBin in range(1, nbin+1):
                SetError_HERAPDF20_VAR_iBin(hlist,iBin,evy_up,evy_dn)

        elif name=='HERAPDF20_NNLO_EIG':
            '''
    HERAPDF20 NNLO (Q2min=3.5) fit and experimental uncertainty variations. The 28 error PDFs should be treated two by two as the up and down excursions along 14 eigenvectors, such that the symmetric error is calculated as the quadrature sum of [Sum i=1,14 of (var i+1 - var i)/2 ], or if asymmetric errors are desired according to Eqn 43 of Campbell, Huston and Stirling hep-ph/0611148. mem=0 ; central; mem=1-28 ; error eigenvectors.
            '''
            ##->Same with hessian  
            for iBin in range(1, nbin+1):
                ## Scan all histo ##
                SetError_hessian_iBin(hlist,iBin,evy_up,evy_dn)
                
        elif name=='HERAPDF20_NNLO_VAR':
            '''HERAPDF20 NNLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all positive (negative) differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error and added in quadrature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.43,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;                mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;     mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5;             mem=6 ; q2cut=5.; mem=7 ; mb=4.25;               mem=8 ; mb=4.75; mem=9 ; mc=1.37;  mem=10; mc=1.49; mem=11 ; par2(Q0 1.6, mc1.43); mem=12 ; par3 (Q0 2.2, mc1.49); mem=13 ; par4(Duv);'''

            
            for iBin in range(1, nbin+1):
                SetError_HERAPDF20_VAR_iBin(hlist,iBin,evy_up,evy_dn)
        elif name=="CT14qed_inc_proton":
            '''
            CT14qed_inc, NLO QCD + LO QED (inclusive photon) sets for the proton,based on CT14nlo with the initial photon PDF defined by the sum of the inelastic photon PDF and the elastic photon PDF, obtained from the equivalent photon approximation, at the initial scale Q0. The initial inelastic photon PDF is defined by the radiative ansatz and parametrized by its initial inelastic momentum fraction. (m=0 ; p=0.00%, mem=1 ; p=0.01%, mem=2 ; p=0.02%, etc., up to mem=30 ; p=0.30%). A limit of p=0.14% was found at the 90% CL in the Reference     
            '''
            for iBin in range(1, nbin+1):
                SetError_CT14qed_inc_iBin(hlist,iBin,evy_up,evy_dn)

    elif combination=='':
        for iBin in range(1, nbin+1):
            evy_up.append(0)
            evy_dn.append(0)

    elif combination=='statonly':
        if iBin==0 :print ">>>>[combination] statonly"

        for iBin in range(1, nbin+1):
            sigma=hlist[0].GetBinError(iBin)
        
            evy_up.append(sigma)
            evy_dn.append(sigma)
    

    else:
        print "[GetCombinedHisto] Cannot Find combination method for "+name+' '+combination




    
    tgrCombine=ROOT.TGraphAsymmErrors(nbin)
    
    #print "len(vx)=",len(vx)
    #print "nbin=",nbin
    
    for iBin in range(0, len(vx)) :
        #print "evy_dn[iBin]=",evy_dn[iBin]
        #print "evy_up[iBin]",evy_up[iBin]
        tgrCombine.SetPoint (iBin,vx[iBin],vy[iBin])
        tgrCombine.SetPointError(iBin, evx[iBin], evx[iBin], evy_dn[iBin], evy_up[iBin])
    
    return tgrCombine
