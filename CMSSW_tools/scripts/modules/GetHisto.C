#include <TH1D.h>
#include <TFile.h>

TH1D* GetHisto(TString filepath, TString HistoName){
  TFile *f=TFile::Open(filepath);
  TH1D*h=(TH1D*)f->Get(HistoName);
  

  return h;



}
