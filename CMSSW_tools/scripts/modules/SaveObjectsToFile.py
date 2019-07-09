'''
void SaveObjectToFile(TString filepath, TObject *a){
  TFile outputFile (filepath,"RECREATE");
  a->Write();
  outputFile.Write();
  outputFile.Close();
}
'''
import ROOT
def SaveObjectsToFile(filepath, object_list):
    outputFile=ROOT.TFile(filepath,'RECREATE')
    

    for obj in object_list:
        obj.Write()
    outputFile.Write()
    outputFile.Close()


