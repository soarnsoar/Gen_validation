#!/usr/bin/env python                                                                                                                                                            


#Nweight=1080




HistoConfig={}
var_names=['pt','mass','eta','phi']
object_names=['Zmuon','Zelectron','dimuon','dielectron','muon1','muon2','electron1','electron2']


for obj in object_names:
    for var in var_names:        
        HistoConfig[obj+"_"+var]={'title':obj+"_"+var,'varname':obj+"_"+var, 'nbin':50, 'xmin':0, 'xmax':100}
        
        if 'di' in obj or 'Z' in obj:##di lepton OR Z boson
            if 'mass' in var:
                HistoConfig[obj+"_"+var]['xmin']=60
                HistoConfig[obj+"_"+var]['xmax']=560
            if 'pt' in var:
                HistoConfig[obj+"_"+var]['xmin']=0
                HistoConfig[obj+"_"+var]['xmax']=300


        else: ##lepton
            if 'mass' in var:
                HistoConfig[obj+"_"+var]['xmin']=0
                HistoConfig[obj+"_"+var]['xmax']=1
            if 'pt' in var:
                HistoConfig[obj+"_"+var]['xmin']=0
                HistoConfig[obj+"_"+var]['xmax']=500
        if 'eta' in var:
            HistoConfig[obj+"_"+var]['xmin']=-5
            HistoConfig[obj+"_"+var]['xmax']=5
        if 'phi' in var:
            HistoConfig[obj+"_"+var]['xmin']=-4
            HistoConfig[obj+"_"+var]['xmax']=4


HistoConfig['Zmuon_mass_60_120']={'title':'Zmuon_mass_60_120','varname':'Zmuon_mass','nbin':60,'xmin':60,'xmax':120}
HistoConfig['dimuon_mass_60_120']={'title':'dimuon_mass_60_120','varname':'dimuon_mass','nbin':60,'xmin':60,'xmax':120}
HistoConfig['Zelectron_mass_60_120']={'title':'Zelectron_mass_60_120','varname':'Zelectron_mass','nbin':60,'xmin':60,'xmax':120}
HistoConfig['dielectron_mass_60_120']={'title':'dielectron_mass_60_120','varname':'dielectron_mass','nbin':60,'xmin':60,'xmax':120}

#print len(HistoConfig)
