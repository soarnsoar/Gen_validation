#include <TH1D.h>
#include <TFile.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
TH1D* GetHisto(TString filepath, TString HistoName){
  //TFile *f=TFile::Open(filepath);
  TFile f(filepath);
  TH1D*h=(TH1D*)f.Get(HistoName);
  h->SetDirectory(0);
  f.Close();
  return h;



}


TGraphErrors* GetTGraphErrors(TString filepath, TString HistoName){
  //TFile *f=TFile::Open(filepath);
  TFile f(filepath);
  TGraphErrors*h=(TGraphErrors*)f.Get(HistoName);
  //h->SetDirectory(0);
  f.Close();
  return h;



}

TGraphAsymmErrors* GetTGraphAsymmErrors(TString filepath, TString HistoName){
  //TFile *f=TFile::Open(filepath);
  TFile f(filepath);
  TGraphAsymmErrors*h=(TGraphAsymmErrors*)f.Get(HistoName);
  //h->SetDirectory(0);
  f.Close();
  return h;



}


