#include <TObject.h>
#include <TString.h>
#include <TFile.h>
void SaveObjectToFile(TString filepath, TObject *a){
  TFile outputFile (filepath,"RECREATE");
  a->Write();
  outputFile.Write();
  outputFile.Close();
}
