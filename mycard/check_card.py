import glob
import os

current_dir=os.getcwd()

dirs=glob.glob('*/')

list_True=['true','T','True']
list_False=['false','F','False']

def check_pdfwgt(runcard):
    #print "[check_pdfwgt]"
    isFine=False
    lines=open(runcard).readlines()
    
    for line in lines:
        if 'pdfwgt' in line:
            if 'pdfwgt_T' in runcard:
                #print "pdfwgt==T"
                for true in list_True:
                    if true in line : isFine=True
                if not isFine:
                    print '[Error] pdfwgt==T is not specified in proc name'
            
            else:
                #print "pdfwgt==F"
                for false in list_False:
                    if false in line : isFine=True
                    

    return isFine
 
def check_pdfsetting(runcard):
    #print "[check_pdfsetting]"
    
    check_pdlabel=False
    check_lhaid=False
    check_reweight_PDF=False

    lines=open(runcard).readlines()

    for line in lines:
        if 'pdlabel' in line:
            if 'lhapdf' in line : check_pdlabel=True
        if 'lhaid' in line:
            if '$DEFAULT_PDF_SETS' in line : check_lhaid=True
        if 'reweight_PDF' in line:
            if '$DEFAULT_PDF_MEMBERS' in line : check_reweight_PDF=True

    if not check_pdlabel:
        print "'lhapdf'    = pdlabel is missing"
    if not check_lhaid:
        print "$DEFAULT_PDF_SETS = lhaid is missing"
    if not check_reweight_PDF:
        print "$DEFAULT_PDF_MEMBERS = reweight_PDF is missing"

    return check_pdlabel*check_lhaid*check_reweight_PDF
        


   
def check_store_rwgt_info(runcard):
    #print "[check_store_rwgt_info]"
    
    isFine=False

    lines=open(runcard).readlines()
    for line in lines:
        if 'store_rwgt_info' in line:
            for true in list_True:
                if true in line : isFine=True

    return isFine



def check_pdfwgt_TrueFalse(proc):
    print "[check_pdfwgt_TrueFalse]"
    proc_T=proc+'_pdfwgt_T'
    if os.path.isdir(proc_T):
        #print "pdfwgt==T exists"
        return
    elif 'pdfwgt_T' in proc:
        return
    elif 'nlo' in proc.lower() or 'fxfx' in proc.lower():
        return 
    
    else:
        
        orig_dir=os.getcwd()






        proccard_F=proc+'_proc_card.dat'
        runcard_F=proc+'_run_card.dat'
        proccard_T=proc+'_pdfwgt_T_proc_card.dat'
        runcard_T=proc+'_pdfwgt_T_run_card.dat'


        os.system('cp -r '+proc+' '+proc_T)
        os.chdir(proc_T)

        ##--copy cards
        card_list=glob.glob(proc+'*.dat')
        for card in card_list:
            old_card=card
            suffix=card.split(proc)[1]
            new_card=proc_T+suffix
            print new_card
            os.system('mv '+old_card+' '+new_card)


        ##--modify proccard
        f_proc_old=open(proccard_T,'r')
        print proccard_T
        print os.getcwd()
        f_proc_new=open(proccard_T+'_temp','w')
        lines=f_proc_old.readlines()
        for line in lines:
            
            f_proc_new.write(line.replace(proc,proc_T))
    
        f_proc_old.close()
        f_proc_new.close()
        os.system('mv '+proccard_T+'_temp'+' '+proccard_T)
        
        ##--modify runcard
        f_run_old=open(runcard_T,'r')
        f_run_new=open(runcard_T+'_temp','w')
        lines=f_run_old.readlines()
        for line in lines:
 
            if 'pdfwgt' in line and '=' in line:
                f_run_new.write('T = pdfwgt\n')
            else:
                f_run_new.write(line)
        
        
        f_run_old.close()
        f_run_new.close()
        os.system('mv '+runcard_T+'_temp'+' '+runcard_T)
        

        os.chdir(orig_dir)




for directory in dirs:
    proc=directory.split('/')[0]

    print '===['+proc+']==='



    os.chdir(directory)
    if not os.path.isfile(proc+'_proc_card.dat'):
        print "[ERR]NO proc card for "+proc
        exit()
    if not os.path.isfile(proc+'_run_card.dat'):
        print "[ERR]NO proc card for "+proc
        exit()



    runcard=proc+'_run_card.dat'
    if not check_pdfsetting(runcard):
        print "[Error]pdfsetting is missing"
        exit()
    if 'nlo' in runcard.lower() or 'fxfx' in runcard.lower():
        #print "--NLO Process--"
        if not check_store_rwgt_info(runcard):
            print "[Error]wrong store_rwgt_info setting"
            exit()
    elif 'mlm' in runcard.lower() or '_lo' in runcard.lower():
        #print '--LO process--'
        if not check_pdfwgt(runcard):
            print "[Error]wrong pdfwgt setting"
            exit()

            
    
    else:
        print "[WARNING] LO/NLO is not specified"
    os.chdir(current_dir)
    #print "[proc=",proc
    check_pdfwgt_TrueFalse(proc)
