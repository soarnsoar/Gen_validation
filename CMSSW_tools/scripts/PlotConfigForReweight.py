xname=[]
var_names=['pt','mass','eta','phi']
object_names=['Zmuon','Zelectron','dimuon','dielectron','muon1','muon2','electron1','electron2']

for var in var_names:
    for obj in object_names:
        xname.append(obj+'_'+var)



##---weight info
rwgt_info={}

rwgt_info['mg260LO']={}
rwgt_info['mg261LO']={}
rwgt_info['mg265LO']={}
rwgt_info['mg260NLO']={}
rwgt_info['mg261NLO']={}
rwgt_info['mg265NLO']={}

rwgt_info['mg260LO']['process']={ ##Processes and their Histogram path
'dyellell01234j_5f_LO_MLM':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell01234j_5f_LO_MLM__5000evt/combined_histo.root',
}

rwgt_info['mg261LO']['process']={ ##Processes and their Histogram path
'dyellell01234j_5f_LO_MLM':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg261_dyellell01234j_5f_LO_MLM__5000evt/combined_histo.root',
}
rwgt_info['mg265LO']['process']={ ##Processes and their Histogram path
'dyellell01234j_5f_LO_MLM':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg265_dyellell01234j_5f_LO_MLM__5000evt/combined_histo.root',
}



##----MG260LO----##
##Type of systematic cal.
#https://arxiv.org/pdf/1412.7420.pdf
#symhessian:sigma = sigma+ = sigma- = sqrt[ Sum{i=1~N}( F_i - F_0  )^2   ]
#replica   :sigma = sigma+ = sigma- = sqrt[  N_rep/(N_rep-1)  * (<F^2> - <F>^2   )   ]
#hessian   :up-element & down-element
##sigma+ = sqrt[ Sum[ max(F_i_up - F_0 , F_i_down - F_0, 0 )^2   ]   ]
##sigma- = sqrt[ Sum[ max(F_0 - F_i_up , F+0 - F_i_down, 0 )^2   ]   ]

rwgt_info['mg260LO']['variation']['muRmuF_default']={
    'combination':'envelope', 
    'name':'default_scale',
    'idx':[0,5,10,15,20,25,30,35,40],
    
}
rwgt_info['mg260LO']['variation']['muRmuF_sumpt']={
    'combination':'envelope',
    'name':'sumpt_scale',
    'idx':  [1,6,11,16,21,26,31,36,41],
    
}
rwgt_info['mg260LO']['variation']['muRmuF_HT']={
    'combination':'envelope',
    'name':'HT_scale',
    'idx':     [2,7,12,17,22,27,32,37,42],
    
}
rwgt_info['mg260LO']['variation']['muRmuF_HTover2']={
    'combination':'envelope',
    'name':'HT/2_scale',
    'idx':   [3,8,13,18,23,28,33,38,43],
    
}
rwgt_info['mg260LO']['variation']['muRmuF_sqrts']={
    'combination':'envelope',
    'name':'sqrts_scale',
    'idx':  [4,9,14,19,24,29,34,39,44],
}


rwgt_info['mg260LO']['variation']['306000']={
    'name':'NNPDF31_nnlo_hessian_pdfas',
    'combination':'symmhessian+as',
    'idx':range(45,148), ##45~147
}

rwgt_info['mg260LO']['variation']['322500']={
    'name':'NNPDF31_nnlo_as_0108',
    'combination':"",
    'idx':[148]
}
rwgt_info['mg260LO']['variation']['322700']={
    'name':'NNPDF31_nnlo_as_0110',
    'combination':"",
    'idx':[149]
}
rwgt_info['mg260LO']['variation']['322900']={
    'name':'NNPDF31_nnlo_as_0112',
    'combination':"",
    'idx':[150]
}
rwgt_info['mg260LO']['variation']['323100']={
    'name':'NNPDF31_nnlo_as_0114',
    'combination':"",
    'idx':[151]
}
rwgt_info['mg260LO']['variation']['323300']={
    'name':'NNPDF31_nnlo_as_0117',
    'combination':"",
    'idx':[152]
}
rwgt_info['mg260LO']['variation']['323500']={
    'name':'NNPDF31_nnlo_as_0119',
    'combination':"",
    'idx':[153]
}
rwgt_info['mg260LO']['variation']['323700']={
    'name':'NNPDF31_nnlo_as_0122',
    'combination':"",
    'idx':[154]
}
rwgt_info['mg260LO']['variation']['323900']={
    'name':'NNPDF31_nnlo_as_0124',
    'combination':"",
    'idx':[155]
}
rwgt_info['mg260LO']['variation']['305800']={
    'name':'NNPDF31_nlo_hessian_pdfas',
    'combination':"symmhessian+as",
    'idx':range(156,259)
}
rwgt_info['mg260LO']['variation']['13000']={
    'name':'CT14nnlo',
    'combination':"hessian",
    'idx':range(259,316)
}
rwgt_info['mg260LO']['variation']['13065']={
    'name':'CT14nnlo as=0.116',
    'combination':"",
    'idx':[316]
}
rwgt_info['mg260LO']['variation']['13069']={
    'name':'CT14nnlo as=0.120',
    'combination':"",
    'idx':[317]
}
rwgt_info['mg260LO']['variation']['13100']={
    'name':'CT14nlo',
    'combination':"hessian",
    'idx':range(318,375)
}
rwgt_info['mg260LO']['variation']['13163']={
    'name':'CT14nlo as=0.116',
    'combination':"",
    'idx':[375]
}
rwgt_info['mg260LO']['variation']['13167']={
    'combination':"CT14nlo as=0.120",
    'idx':[376]
}
rwgt_info['mg260LO']['variation']['13200']={
       'name':'CT14lo',
    'combination':"",
    'idx':[377]
}
rwgt_info['mg260LO']['variation']['25200']={
    'name':'MMHT2014nlo68clas118',
    'combination':"hessian",
    'idx':range(378,429)
}
rwgt_info['mg260LO']['variation']['25300']={
    'name':'MMHT2014nnlo68cl',
    'combination':"hessian",
    'idx':range(429,480)
}
rwgt_info['mg260LO']['variation']['25000']={
    'name':'MMHT2014lo68cl',
    'combination':"",
    'idx':[480]
}
rwgt_info['mg260LO']['variation']['42780']={
    'name':'ABMP16als118_5_nnlo',
    'combination':"symmhessian",
    'idx':range(481,511)
}
rwgt_info['mg260LO']['variation']['90200']={
    'name':'PDF4LHC15_nlo_100_pdfas',
    'combination':"symmhessian+as",
    'idx':range(511,614)
}
rwgt_info['mg260LO']['variation']['91200']={
    'name':'PDF4LHC15_nnlo_100_pdfas',
    'combination':"symmhessian+as",
    'idx':range(614,717)
}
rwgt_info['mg260LO']['variation']['90400']={
    'name':'PDF4LHC15_nlo_30_pdfas',
    'combination':"symmhessian+as",
    'idx':range(717,750)
}

rwgt_info['mg260LO']['variation']['91400']={
    'name':'PDF4LHC15_nnlo_30_pdfas',
    'combination':"symmhessian+as",
    'idx':range(750,783)
}
rwgt_info['mg260LO']['variation']['61100']={
    'name':'HERAPDF20_NLO_EIG',
    'combination':"symmhessian+as",
    'idx':range(783,812)
}
rwgt_info['mg260LO']['variation']['61130']={
    'name':'HERAPDF20_NLO_VAR',
    'combination':"custom",
    'idx':range(812,826),
    'comment':'''
    HERAPDF20 NLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all positive (negative) differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error and added in quadrature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.47,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;  mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5; mem=6 ; q2cut=5.; mem=7 ; mb=4.25;mem=8 ; mb=4.75; mem=9 ; mc=1.41;  mem=10 ; mc=1.53; mem=11 ; par2(Q0 1.6, mc1.47); mem=12 ; par3 (Q0 2.2, mc1.53); mem=13 ; par4(Duv);
    '''
}

rwgt_info['mg260LO']['variation']['61100']={
    'name':'HERAPDF20_NNLO_EIG',
    'combination':"custom",
    'idx':range(826,855),
    'comment':'''
    HERAPDF20 NNLO (Q2min=3.5) fit and experimental uncertainty variations. The 28 error PDFs should be treated two by two as the up and down excursions along 14 eigenvectors, such that the symmetric error is calculated as the quadrature sum of [Sum i=1,14 of (var i+1 - var i)/2 ], or if asymmetric errors are desired according to Eqn 43 of Campbell, Huston and Stirling hep-ph/0611148. mem=0 ; central; mem=1-28 ; error eigenvectors.
    '''
}

rwgt_info['mg260LO']['variation']['61230']={
    'name':'HERAPDF20_NNLO_VAR',
    'combination':"custom",
    'idx':range(855,869),
    'comment':'''HERAPDF20 NNLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all positive (negative) differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error and added in quadrature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.43,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;                mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;     mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5;             mem=6 ; q2cut=5.; mem=7 ; mb=4.25;               mem=8 ; mb=4.75; mem=9 ; mc=1.37;  mem=10 ; mc=1.49; mem=11 ; par2(Q0 1.6, mc1.43); mem=12 ; par3 (Q0 2.2, mc1.49); mem=13 ; par4(Duv);
    '''
}


rwgt_info['mg260LO']['variation']['13400']={
    'name':'CT14qed_inc_proton',
    'combination':"custom",
    'idx':range(869,900),
    'comment':'''
CT14qed_inc, NLO QCD + LO QED (inclusive photon) sets for the proton,based on CT14nlo with the initial photon PDF defined by the sum of the inelastic photon PDF and the elastic photon PDF, obtained from the equivalent photon approximation, at the initial scale Q0. The initial inelastic photon PDF is defined by the radiative ansatz and parametrized by its initial inelastic momentum fraction. (m=0 ; p=0.00%, mem=1 ; p=0.01%, mem=2 ; p=0.02%, etc., up to mem=30 ; p=0.30%). A limit of p=0.14% was found at the 90% CL in the Reference
    '''
}

rwgt_info['mg260LO']['variation']['82200']={
    'name':'LUXqed17_plus_PDF4LHC15_nnlo_100',
    'combination':"symmhessian",
    'idx':range(900,1008),
    'comment':'''
  0 is central
  1-100 map to original PDF members
  101 replacement of CLAS resonance fit with Christy-Bosted fit
  102 rescale-R-0.5
  103 rescale R in high-Q^2 region with a higher-twist component
  104 use the A1 elastic fit result without the two-photon exchange corrections
  105 use the lower edge of the elastic fit error band
  106 lower the transition from Hermes GD11-P to the PDF-based F2,FL determinations to 5 GeV^2
  107 extremum of absolute variation obtained by adding the NNLO QCD contribution for each of three scale choices (mu_M/mu = 0.5, 1.0, 2.0)                                                                                                                            
    '''
}

rwgt_info['mg260LO']['variation']['292200']={
    'name':'NNPDF30_nlo_nf_5_pdfas',
    'combination':"replicas+as",
    'idx':range(1008,1116),

}


#---mg261LO
rwgt_info['mg261LO']['variation']=rwgt_info['mg260LO']['variation']

#--mg265LO
rwgt_info['mg265LO']['variation']=rwgt_info['mg260LO']['variation']


#---mg260NLO

rwgt_info['mg260NLO']['process']={ ##Processes and their Histogram path                                                                                                           
'dyellell012j_5f_NLO_FXFX':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell012j_5f_NLO_FXFX__5000evt__5000evt/combined_histo.root',
}
rwgt_info['mg261NLO']['process']={ ##Processes and their Histogram path                                                                                                           
'dyellell012j_5f_NLO_FXFX':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell012j_5f_NLO_FXFX__5000evt__5000evt/combined_histo.root',
}
rwgt_info['mg265NLO']['process']={ ##Processes and their Histogram path                                                                                                           
'dyellell012j_5f_NLO_FXFX':'/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell012j_5f_NLO_FXFX__5000evt__5000evt/combined_histo.root',
}



rwgt_info['mg260NLO']['variation']['muRmuF']={
    'combination':'envelope',
    'name':'scale',
    'idx':range(0,9),
    
}

rwgt_info['mg260NLO']['variation']['306000']={
    'name':'NNPDF31_nnlo_hessian_pdfas',
    'combination':'symmhessian+as',
    'idx':range(9,112), 
}

rwgt_info['mg260NLO']['variation']['322500']={
    'name':'NNPDF31_nnlo_as_0108',
    'combination':"NNPDF31_nnlo_as_0110",
    'idx':[112]
}
rwgt_info['mg260NLO']['variation']['322700']={

    'name':'NNPDF31_nnlo_as_0110',
    'combination':"",
    'idx':[113]
}
rwgt_info['mg260NLO']['variation']['322900']={
    'name':'NNPDF31_nnlo_as_0112',
    'combination':"",
    'idx':[114]
}
rwgt_info['mg260NLO']['variation']['323100']={
    'name':'NNPDF31_nnlo_as_0114',
    'combination':"",
    'idx':[115]
}
rwgt_info['mg260NLO']['variation']['323300']={
    'name':'NNPDF31_nnlo_as_0117',
    'combination':"",
    'idx':[116]
}
rwgt_info['mg260NLO']['variation']['323500']={
    'name':'NNPDF31_nnlo_as_0119',
    'combination':"",
    'idx':[117]
}
rwgt_info['mg260NLO']['variation']['323700']={
    'name':'NNPDF31_nnlo_as_0122',
    'combination':"",
    'idx':[118]
}
rwgt_info['mg260NLO']['variation']['323900']={
    'name':'NNPDF31_nnlo_as_0124',
    'combination':"",
    'idx':[119]
}
rwgt_info['mg260NLO']['variation']['305800']={
    'name':'NNPDF31_nlo_hessian_pdfas',
    'combination':"symmhessian+as",
    'idx':range(120,223)
}
rwgt_info['mg260NLO']['variation']['13000']={
    'name':'CT14nnlo',
    'combination':"hessian",
    'idx':range(223,280)
}
rwgt_info['mg260NLO']['variation']['13065']={
    'name':'CT14nnlo as=0.116',
    'combination':"",
    'idx':[280]
}
rwgt_info['mg260NLO']['variation']['13069']={
    'name':'CT14nnlo as=0.120',
    'combination':"",
    'idx':[281]
}
rwgt_info['mg260NLO']['variation']['13100']={
    'name':'CT14nlo',
    'combination':"hessian",
    'idx':range(282,339)
}
rwgt_info['mg260NLO']['variation']['13163']={
    'name':'CT14nlo as=0.116',
    'combination':"",
    'idx':[339]
}
rwgt_info['mg260NLO']['variation']['13167']={
    'combination':"CT14nlo as=0.120",
    'idx':[340]
}
rwgt_info['mg260NLO']['variation']['13200']={
       'name':'CT14lo',
    'combination':"",
    'idx':[341]
}
rwgt_info['mg260NLO']['variation']['25200']={
    'name':'MMHT2014nlo68clas118',
    'combination':"hessian",
    'idx':range(342,393)
}
rwgt_info['mg260NLO']['variation']['25300']={
    'name':'MMHT2014nnlo68cl',
    'combination':"hessian",
    'idx':range(393,444)
}
rwgt_info['mg260NLO']['variation']['25000']={
    'name':'MMHT2014lo68cl',
    'combination':"",
    'idx':[444]
}
rwgt_info['mg260NLO']['variation']['42780']={
    'name':'ABMP16als118_5_nnlo',
    'combination':"symmhessian",
    'idx':range(445,475)
}
rwgt_info['mg260NLO']['variation']['90200']={
    'name':'PDF4LHC15_nlo_100_pdfas',
    'combination':"symmhessian+as",
    'idx':range(475,578)
}
rwgt_info['mg260NLO']['variation']['91200']={
    'name':'PDF4LHC15_nnlo_100_pdfas',
    'combination':"symmhessian+as",
    'idx':range(578,681)
}
rwgt_info['mg260NLO']['variation']['90400']={
    'name':'PDF4LHC15_nlo_30_pdfas',
    'combination':"symmhessian+as",
    'idx':range(681,714)
}

rwgt_info['mg260NLO']['variation']['91400']={
    'name':'PDF4LHC15_nnlo_30_pdfas',
    'combination':"symmhessian+as",
    'idx':range(714,747)
}
rwgt_info['mg260NLO']['variation']['61100']={
    'name':'HERAPDF20_NLO_EIG',
    'combination':"symmhessian+as",
    'idx':range(747,776)
}
rwgt_info['mg260NLO']['variation']['61130']={
    'name':'HERAPDF20_NLO_VAR',
    'combination':"custom",
    'idx':range(776,790),
    'comment':'''                                                                                                                                                                                                                                                                             
    HERAPDF20 NLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all positive (negative)\
 differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error and added in qua\
drature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.47,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;  mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5; mem=6 ; q2cut=5.; mem=7 ; mb=4.25;mem=8 ; mb=4.7\
5; mem=9 ; mc=1.41;  mem=10 ; mc=1.53; mem=11 ; par2(Q0 1.6, mc1.47); mem=12 ; par3 (Q0 2.2, mc1.53); mem=13 ; par4(Duv);                                                                                                                                                                     
    '''
}

rwgt_info['mg260NLO']['variation']['61100']={
    'name':'HERAPDF20_NNLO_EIG',
    'combination':"custom",
    'idx':range(790,819),
    'comment':'''                                                                                                                                                                                                                                                                             
    HERAPDF20 NNLO (Q2min=3.5) fit and experimental uncertainty variations. The 28 error PDFs should be treated two by two as the up and down excursions along 14 eigenvectors, such that the symmetric error is calculated as the quadrature sum of [Sum i=1,14 of (var i+1 - var i)/2 ], or\
 if asymmetric errors are desired according to Eqn 43 of Campbell, Huston and Stirling hep-ph/0611148. mem=0 ; central; mem=1-28 ; error eigenvectors.                                                                                                                                        
    '''
}

rwgt_info['mg260NLO']['variation']['61230']={
    'name':'HERAPDF20_NNLO_VAR',
    'combination':"custom",
    'idx':range(819,833),
    'comment':'''HERAPDF20 NNLO variations of fit parameters. Member 0 is the central fit. The 1-10 variations are considered as model errors and should be treated one by one, by taking the difference between the variation and the central value, and then adding in quadrature all posit\
ive (negative) differences to obtain the positive (negative) model error. Variations 11 to 13 are the maximal parametrisation variations; the largest positive (negative) difference between the variation and the central value is taken as the positive (negative) parametrisation error an\
d added in quadrature to the model errors to form the parametrisation envelope. mem=0 ; central (fs=0.4,mb=4.5,mc=1.43,q20=1.9,q2min=3.5,a_s(MZ)=0.118); mem=1 ; fs=0.3;                mem=2 ; fs=0.5; mem=3 ; fs=hermesfs-03;     mem=4 ; fs=hermesfs-05 mem=5 ; q2cut=2.5;             mem\
=6 ; q2cut=5.; mem=7 ; mb=4.25;               mem=8 ; mb=4.75; mem=9 ; mc=1.37;  mem=10 ; mc=1.49; mem=11 ; par2(Q0 1.6, mc1.43); mem=12 ; par3 (Q0 2.2, mc1.49); mem=13 ; par4(Duv);                                                                                                         
    '''
}


rwgt_info['mg260NLO']['variation']['13400']={
    'name':'CT14qed_inc_proton',
    'combination':"custom",
    'idx':range(833,864),
    'comment':'''                                                                                                                                                                                                                                                                             
CT14qed_inc, NLO QCD + LO QED (inclusive photon) sets for the proton,based on CT14nlo with the initial photon PDF defined by the sum of the inelastic photon PDF and the elastic photon PDF, obtained from the equivalent photon approximation, at the initial scale Q0. The initial inelasti\
c photon PDF is defined by the radiative ansatz and parametrized by its initial inelastic momentum fraction. (m=0 ; p=0.00%, mem=1 ; p=0.01%, mem=2 ; p=0.02%, etc., up to mem=30 ; p=0.30%). A limit of p=0.14% was found at the 90% CL in the Reference                                     
    '''
}

rwgt_info['mg260NLO']['variation']['82200']={
    'name':'LUXqed17_plus_PDF4LHC15_nnlo_100',
    'combination':"symmhessian",
    'idx':range(864,972),
    'comment':'''                                                                                                                                                                                                                                                                             
  0 is central                                                                                                                                                                                                                                                                                
  1-100 map to original PDF members                                                                                                                                                                                                                                                           
  101 replacement of CLAS resonance fit with Christy-Bosted fit                                                                                                                                                                                                                               
  102 rescale-R-0.5                                                                                                                                                                                                                                                                           
  103 rescale R in high-Q^2 region with a higher-twist component                                                                                                                                                                                                                              
  104 use the A1 elastic fit result without the two-photon exchange corrections                                                                                                                                                                                                               
  105 use the lower edge of the elastic fit error band                                                                                                                                                                                                                                        
  106 lower the transition from Hermes GD11-P to the PDF-based F2,FL determinations to 5 GeV^2                                                                                                                                                                                                
  107 extremum of absolute variation obtained by adding the NNLO QCD contribution for each of three scale choices (mu_M/mu = 0.5, 1.0, 2.0)                                                                                                                                                   
    '''
}

rwgt_info['mg260NLO']['variation']['292200']={
    'name':'NNPDF30_nlo_nf_5_pdfas',
    'combination':"replicas+as",
    'idx':range(972,1080),

}

rwgt_info['mg261NLO']['variation']=rwgt_info['mg260NLO']['variation']
rwgt_info['mg265NLO']['variation']=rwgt_info['mg260NLO']['variation']
