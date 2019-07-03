// -*- C++ -*-
//
// Package:    Analyzer/weight_assign_242LO
// Class:      weight_assign_242LO
// 
/**\class weight_assign_242LO weight_assign_242LO.cc Analyzer/weight_assign_242LO/plugins/weight_assign_242LO.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  JunHo Choi
//         Created:  Fri, 23 Mar 2018 03:24:18 GMT
//
//

//vector<reco::GenParticle>             "prunedGenParticles"        ""                "PAT"     

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"


using namespace edm;
using namespace reco;
using namespace std;

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Run.h"//to use edm::Run


#include <TTree.h>
#include <TFile.h>
#include <TLorentzVector.h>
//#include "GEN_Analyzer/JHanalyzer/interface/weightinfo.h"

//
// Class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.



//class HistoFactoryDYKinematics : public edm::one::EDAnalyzer<edm::one::SharedResources>  {

class HistoFactoryDYKinematics : public edm::one::EDAnalyzer<edm::one::WatchRuns,edm::one::SharedResources>  {
//class HistoFactoryDYKinematics : public edm::EDAnalyzer  {
   public:
      explicit HistoFactoryDYKinematics(const edm::ParameterSet&);
      ~HistoFactoryDYKinematics();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
 
  //  virtual void beginJob(edm::Run const& iEvent, edm::EventSetup const &) override;
  //  void beginRun(edm::Run const&, edm::EventSetup const&) override;//to get LHERunInfoProduct//add new method
  //void endRun(edm::Run const&, edm::EventSetup const&) override;
private:
  virtual void beginJob() override;
  //  virtual void beginJob(edm::Run const& iRun) override;
  //  virtual void beginJob(edm::Run const& iRun, edm::EventSetup const &iSetup) ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
  //  virtual void doBeginRun_(edm::Run const&, edm::EventSetup const&) override;
  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginRun(edm::Run const& iEvent, edm::EventSetup const&) override;
  //virtual void beginRun(edm::Run const& iRun, edm::EventSetup const &iSetup ) override;//to get LHERunInfoProduct//add new method
  //virtual void beginRun() override;//to get LHERunInfoProduct//add new method
  //GenEventInfoProduct                   "generator"                 ""                "SIM"   

//  void beginRun(edm::Run const& iEvent, edm::EventSetup const&) override;

  //edm::EDGetTokenT<GenParticleCollection> genParticles_Token;
  edm::EDGetTokenT<vector<reco::GenParticle>> genParticles_Token;
  edm::EDGetTokenT<GenEventInfoProduct> genInfo_Token;
  edm::EDGetTokenT<LHEEventProduct> LHEInfo_Token;


  //TFile * outputFile_;
  //TH1D * h_pt;
  //TH1D** v_h_pt[100];
  //vector<TH1D*> v_h_pt;
  //TList *hlist;

  //<JHCHOI_HISTO_DECLARE>//
  
  
      // ----------member data ---------------------------
};
//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
HistoFactoryDYKinematics::HistoFactoryDYKinematics(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
 
  //vector<reco::GenParticle>             "genParticles"              ""                "SIM"     

  usesResource("TFileService");
  genParticles_Token = consumes<vector<reco::GenParticle>>(edm::InputTag("genParticles"));
  genInfo_Token = consumes<GenEventInfoProduct>(edm::InputTag("generator"));
  LHEInfo_Token = consumes<LHEEventProduct>(edm::InputTag("externalLHEProducer"));

  edm::Service<TFileService> fs;
  //v_h_pt=fs->make<vector<TH1D*>>;
  //v_h_pt=fs->make<std::vector<TH1D>>;
  //hlist=fs->make<TList>
  //<JHCHOI_HISTO_DEFINE>//
  

  //h_pt=fs->make<TH1D>("h_pt" , "h_pt" , 100 , 0 , 5000 );
  //v_h_pt=fs->make<TH1D**>;
  //v_h_pt[0]=new TH1D("a","a",100,0,100);
  //extLHEInfo_Token = consumes<LHERunInfoProduct>(edm::InputTag("externalLHEProducer"));  
  //  extLHEInfo_Token= consumes<LHERunInfoProduct,edm::InRun>(edm::InputTag("externalLHEProducer",""));
 
 //Let's make vector for find weights!//
  //make_weight_infos();
 

}


HistoFactoryDYKinematics::~HistoFactoryDYKinematics()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
HistoFactoryDYKinematics::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  /*
  double Zmuon_pt,Zmuon_mass,Zmuon_eta,Zmuon_phi;
  double muon1_pt,muon1_eta,muon1_phi;
  double muon2_pt,muon2_eta,muon2_phi;
  double dimuon_pt,dimuon_mass,dimuon_eta,dimuon_phi;


  double Zelectron_pt,Zelectron_mass,Zelectron_eta,Zelectron_phi;
  double electron1_pt,electron1_eta,electron1_phi;
  double electron2_pt,electron2_eta,electron2_phi;
  double dielectron_pt,dielectron_mass,dielectron_eta,dielectron_phi;

  Zmuon_pt=0;Zmuon_mass=0;Zmuon_eta=0;Zmuon_phi=0;
  muon1_pt=0;muon1_eta=0;muon1_phi=0;
  muon2_pt=0;muon2_eta=0;muon2_phi=0;
  dimuon_pt=0;dimuon_mass=0;dimuon_eta=0;dimuon_phi=0;

 
  Zelectron_pt=0;Zelectron_mass=0;Zelectron_eta=0;Zelectron_phi=0;
  electron1_pt=0;electron1_eta=0;electron1_phi=0;
  electron2_pt=0;electron2_eta=0;electron2_phi=0;
  dielectron_pt=0;dielectron_mass=0;dielectron_eta=0;dielectron_phi=0;
  */
  

  edm::Handle<LHEEventProduct> LHEInfo;
  iEvent.getByToken(LHEInfo_Token, LHEInfo);

  //veto tau events//                             
  const lhef::HEPEUP& lheEvent = LHEInfo->hepeup();
  std::vector<lhef::HEPEUP::FiveVector> lheParticles = lheEvent.PUP;
  Int_t nLHEParticle = lheParticles.size();
  for( Int_t idxParticle = 0; idxParticle < nLHEParticle; ++idxParticle ){

    Int_t id = lheEvent.IDUP[idxParticle];
    if(fabs(id)==15) return;
  }
  //////////end of veto tau/////

  ////////////initialize/////////////
  //Get weight//


  //int lheinfoweightsize= LHEInfo->weights().size();
  //int lheinfocommentssize = LHEInfo->comments_size();

  double w0=LHEInfo->originalXWGTUP();
  
  //  for (int i =0; i < lheinfoweightsize; i++){
    //cout<< LHEInfo->weights()[i].id<<endl;
    //    cout<< LHEInfo->weights()[i].wgt/w0<<endl;
  //}
  
  //cout<<"lheinfoweightsize="<<lheinfoweightsize<<endl;
  //for (int i_lhe =0; i_lhe < lheinfoweightsize; i_lhe++){         
    //cout<<LHEInfo->weights()[i_lhe].wgt/w0<<endl;    
  //}
  
  bool isDYelectronEvent=false;
  bool isDYmuonEvent=false;

  
  
   using namespace edm;
   //Handle<reco::GenParticleCollection> genParticles;
   Handle<vector<reco::GenParticle>> genParticles;
   iEvent.getByToken(genParticles_Token, genParticles);//genParticle                                                                                         
   edm::Handle<GenEventInfoProduct> genInfo;
   iEvent.getByToken(genInfo_Token, genInfo);
   //GenEventInfoProduct                   "generator"                 ""                "SIM"   //
   
   double weight=genInfo->weight();
   if(weight<-99) cout<<weight<<endl;
   //   cout<<"weight="<<weight<<endl;

   vector<int> i_muons1;
   vector<int> i_muons2;
   vector<int> i_electrons1;
   vector<int> i_electrons2;
   vector<int> i_photons;
   
   int gensize= genParticles->size();
   cout<<"gensize="<<gensize<<endl;
   for(int i = 0; i < gensize; ++ i) {///scan all gen particles
     //tau veto   
     const GenParticle & p = (*genParticles)[i];
     int id = p.pdgId();
     int status = p.status();
     if(status!=1) continue;
     //double px = p.px();
     ///double py = p.py();
     //double pz = p.pz();
     //double ee = p.energy();
     if(id==11) i_electrons1.push_back(i);
     else if(id== -11) i_electrons2.push_back(i);
     else if(id== 13) i_muons1.push_back(i);
     else if(id== -13) i_muons2.push_back(i);
     else if (id==22)  i_photons.push_back(i);
   }


   if ( i_muons1.size()>0 && i_muons2.size() >0  ) isDYmuonEvent = true;
   if ( i_electrons1.size() > 0 && i_electrons2.size()>0 ) isDYelectronEvent = true;



   if( !isDYmuonEvent && !isDYelectronEvent){
     return;
   }

   
   
   int i_muon1=0;   
   int i_muon2=0;
   if(isDYmuonEvent){
     i_muon1=i_muons1[0];
     i_muon2=i_muons2[0];
   }
   int i_electron1=0;
   int i_electron2=0;
   if(isDYelectronEvent){
     i_electron1=i_electrons1[0];
     i_electron2=i_electrons2[0];
   }
   //Set 1st lep1 and lep2 as DY leptons(simply..)
   //The same as DY validation code :https://github.com/cms-sw/cmssw/blob/02d4198c0b6615287fd88e9a8ff650aea994412e/Validation/EventGenerator/plugins/DrellYanValidation.cc

   TLorentzVector v_electron1,v_electron2,v_muon1,v_muon2;
   v_electron1.SetPxPyPzE((*genParticles)[i_electron1].px(), (*genParticles)[i_electron1].py(),(*genParticles)[i_electron1].pz(),(*genParticles)[i_electron1].energy());
   v_electron2.SetPxPyPzE((*genParticles)[i_electron2].px(), (*genParticles)[i_electron2].py(),(*genParticles)[i_electron2].pz(),(*genParticles)[i_electron2].energy());
   v_muon1.SetPxPyPzE((*genParticles)[i_muon1].px(), (*genParticles)[i_muon1].py(),(*genParticles)[i_muon1].pz(),(*genParticles)[i_muon1].energy());
   v_muon2.SetPxPyPzE((*genParticles)[i_muon2].px(), (*genParticles)[i_muon2].py(),(*genParticles)[i_muon2].pz(),(*genParticles)[i_muon2].energy());

   //   if((v1+v2).M()< 60 ) return;
   
   TLorentzVector v_dielectron=v_electron1+v_electron2;
   TLorentzVector v_Zelectron=v_electron1+v_electron2;
   TLorentzVector v_dimuon=v_muon1+v_muon2;
   TLorentzVector v_Zmuon=v_muon1+v_muon2;
   //vector<int> i_fsr;
   //photons for dressed lepton//
   int photonsize=i_photons.size();
   cout<<"photonsize="<<photonsize<<endl;
   for(int i =0 ; i < photonsize; i++){
     const GenParticle & p = (*genParticles)[i];
     double px = p.px();
     double py = p.py();
     double pz = p.pz();                                                                                                                     
     double ee = p.energy();                                                                                                                 
     TLorentzVector vfsr;
     vfsr.SetPxPyPzE(px,py,pz,ee);
     double dR_electron1=vfsr.DeltaR(v_electron1);
     double dR_electron2=vfsr.DeltaR(v_electron2);
     double dR_muon1=vfsr.DeltaR(v_muon1);
     double dR_muon2=vfsr.DeltaR(v_muon2);
     if(dR_electron1<0.1 || dR_electron2<0.1){ //i_fsr.push_back(i);
       v_Zelectron+=vfsr;
     }
     if(dR_muon1<0.1 || dR_muon2<0.1){ //i_fsr.push_back(i);
       v_Zmuon+=vfsr;
     }
     
   }


   double Zmuon_pt=v_Zmuon.Perp(); double Zmuon_mass=v_Zmuon.M(); double Zmuon_eta=v_Zmuon.Eta(); double Zmuon_phi=v_Zmuon.Phi();
   double muon1_pt=v_muon1.Perp(); double muon1_mass=v_muon1.M(); double muon1_eta=v_muon1.Eta();double muon1_phi=v_muon1.Phi();
   double muon2_pt=v_muon2.Perp(); double muon2_mass=v_muon2.M(); double muon2_eta=v_muon2.Eta();double muon2_phi=v_muon2.Phi();
   double dimuon_pt=v_dimuon.Perp(); double dimuon_mass=v_dimuon.M(); double dimuon_eta=v_dimuon.Eta(); double dimuon_phi=v_dimuon.Phi();

   
   
   double Zelectron_pt=v_Zelectron.Perp(); double Zelectron_mass=v_Zelectron.M(); double Zelectron_eta=v_Zelectron.Eta(); double Zelectron_phi=v_Zelectron.Phi();
   double electron1_pt=v_electron1.Perp(); double electron1_mass=v_electron1.M(); double electron1_eta=v_electron1.Eta();double electron1_phi=v_electron1.Phi();
   double electron2_pt=v_electron2.Perp(); double electron2_mass=v_electron2.M(); double electron2_eta=v_electron2.Eta();double electron2_phi=v_electron2.Phi();
   double dielectron_pt=v_dielectron.Perp();  double dielectron_mass=v_dielectron.M(); double dielectron_eta=v_dielectron.Eta(); double dielectron_phi=v_dielectron.Phi();
   
   /*
   for(int i =0 ; i < 0 ; i++){
     continue;
     cout<<Zmuon_pt<<Zmuon_mass<<Zmuon_eta<<Zmuon_phi<<muon1_pt<<muon1_eta<<muon1_phi<<muon2_pt<<muon2_eta<<muon2_phi<<dimuon_pt<<dimuon_mass<<dimuon_eta<<dimuon_phi<<endl;
     cout<<Zelectron_pt<<Zelectron_mass<<Zelectron_eta<<Zelectron_phi<<electron1_pt<<electron1_eta<<electron1_phi<<electron2_pt<<electron2_eta<<electron2_phi<<dielectron_pt<<dielectron_mass<<dielectron_eta<<dielectron_phi<<endl;
   }
   */
     //cout<<"electron1_pt="<<electron1_pt<<endl;
   //h_pt->Fill(electron1_pt);
   //v_h_pt[0]->Fill(electron1_pt);
   if(isDYmuonEvent){

     //<isDYmuonEventArea>//
     
   }

   if(isDYelectronEvent){
     //<isDYelectronEventArea>//

     
   }


#ifdef THIS_IS_AN_EVENT_EXAMPLE
   
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   
#endif
   
}





// ------------ method called once each job just before starting event loop  ------------

void 
HistoFactoryDYKinematics::beginJob()
//HistoFactoryDYKinematics::beginJob(edm::Run const& iRun)
//HistoFactoryDYKinematics::beginJob(edm::Run const& iRun, edm::EventSetup const &iSetup)
{
  cout<<"begin job"<<endl;


  cout<<"end of begin job"<<endl;


  

}

// ------------ method called once each job just after ending the event loop  ------------

void 
HistoFactoryDYKinematics::endJob() 
{
  cout<<"endjob"<<endl;
  //outputFile->Write();
  //outputFile->Close();


}



void 
HistoFactoryDYKinematics::beginRun(const Run &iEvent, EventSetup const &iSetup ){
  cout<<" beginrun"<<endl;
  //edm::Handle<LHEEventProduct> LHEInfo;
  //iEvent.getByToken(LHEInfo_Token, LHEInfo);
  //int lheinfoweightsize= LHEInfo->weights().size();
  //cout<<"lheinfoweightsize="<<lheinfoweightsize<<endl;
  //TH1D *h=new TH1D("a","a",100,0,100);
  //v_h_pt.push_back(h);
  
  cout<<"end of beginrun"<<endl;
}



void
HistoFactoryDYKinematics::endRun(edm::Run const& iEvent, edm::EventSetup const&) 
{
  cout<<"doendrun"<<endl;

}
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------


void
HistoFactoryDYKinematics::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


//////defined by jhchoi/////




//define this as a plug-in
DEFINE_FWK_MODULE(HistoFactoryDYKinematics);
