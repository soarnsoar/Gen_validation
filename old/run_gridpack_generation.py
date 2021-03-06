import os
import socket
import subprocess
import argparse




class MG_gridpackGEN():


    def __init__(self,gitbranch,gendirname=None):

        self.card_dir=os.getcwd()+'/mycard'
        self.gengit='git@github.com:cms-sw/genproductions.git'
        self.dir_current=os.getcwd()
        self.gitbranch=gitbranch
        self.gendirname=gendirname
        if gendirname==None:
            self.gendirname=self.gitbranch
        self.myMGdir=os.getcwd()+'/'+self.gendirname+'/bin/MadGraph5_aMCatNLO'
    #self.process_name=''
    def setup_genproductions(self):
        
        if os.path.exists(self.gendirname):return

        command= "git clone "+self.gengit+" -b "+self.gitbranch+' '+self.gendirname
        print "---"+command+"---"
        os.system(command)
        
        
        path=self.dir_current+'/'+self.gendirname+'/bin/MadGraph5_aMCatNLO'
        print '---'+path+'---'
        os.chdir(path)
        

        command='cp -r '+self.card_dir+' .'
        print '---'+command+'---'
        os.system(command)
        
        command='git clone git@github.com:soarnsoar/python_tool.git'
        print command
        os.system(command)
        
        
        command='python python_tool/add_runtime.py submit_condor_gridpack_generation.sh'
        print command
        os.system(command)
        
    
        command='python python_tool/add_runtime.py submit_cmsconnect_gridpack_generation.sh'
        print command
        os.system(command)
        
        if 'lxplus7' in socket.gethostname():

            command= 'find . -name "gridpack_generation.sh" | xargs perl -pi -e s/slc6/slc7/g'
            print command
            os.system(command)

        self.myMGdir=os.getcwd()
        
        command='git clone git@github.com:soarnsoar/Gen_validation.git'
        os.system(command)
        #os.chdir(self.dir_current)##go back to the initial path

        #return myMGdir ## setup dir

    def submit_process(self,process_name):
        print "---submit_process---"

        print '--go to my MG directory--'
        print self.myMGdir
        #os.chdir(self.myMGdir)
        script ='submit_condor_gridpack_generation.sh'
        #execute='k5reauth -f -i 3600 -p jhchoi -k /afs/cern.ch/user/j/${USER}/refresh_auth/${USER}.keytab -- nohup'
        execute ='source'
        if 'login.uscms.org' in socket.gethostname():
            script  = 'submit_cmsconnect_gridpack_generation.sh'
            execute = 'nohup'
        #    nohup ./submit_cmsconnect_gridpack_generation.sh ${proc} mycard/${proc}/ > ${proc}.debug 2>&1 &
        
        

        command=execute+' ./'+script+' '+process_name+' '+self.card_dir.split('/')[-1]+'/'+process_name+' > '+process_name+'.debug 2>&1 &'

        os.chdir(self.dir_current)
        
        #self.gitbranch
        #self.gendirname
        scriptname='run__'+self.gitbranch+"__"+self.gendirname+"__"+process_name+'.sh'
        f=open(scriptname,'w')
        f.write('pushd '+self.myMGdir+'\n')
        f.write('rm -rf '+process_name+'\n')
        f.write('rm '+process_name+'log\n')
        f.write('rm '+process_name+'debug\n')
        f.write('rm '+process_name+'_codegen.sh\n')
        f.write('echo "source '+'Gen_validation/test_one_gridpack.sh "'+process_name+' >> '+script+'\n')
        f.write(command+'\n')
        f.write('popd\n')
        f.close()

        #print '---'+command+'---'
        #os.system(command)
        #subprocess.call(command, shell=True)
        
        



def submit_by_dictionary(conf):       
    myMG=MG_gridpackGEN(conf['branch'],conf['dir'])
    myMG.setup_genproductions()
    
    for p in conf['process']:

        print p
        myMG.submit_process(p)




        
if __name__ == "__main__":
    
    #class MG_gridpackGEN():
    #    self.card_dir=os.getcwd()+'/mycard'
    #    self.gengit='git@github.com:cms-sw/genproductions.git'
    #    self.dir_current=os.getcwd()
    #    self.gitbranch='master'
    #    self.gendirname=self.gitbranch

    #    def __init__(self,gitbranch,gendirname=None):

    #    def setup_genproductions(self):

    #    def submit_process(self,process_name):


    #conf260={'branch':'master','dir':'mg260_master',
    #         'process':[
    #            'dyellell012j_5f_NLO_FXFX'
    #         ],
    #}
    
    
    #conf261={'branch':'mg261' ,'dir':'mg261'       ,
    #         'process':[
    #             #'dyellell012j_5f_LO_MLM',
    #             #'dyellell012j_5f_LO_MLM_pdfwgt_T',
    #             'dyellell012j_5f_NLO_FXFX',
    #         ],
    #}

    
    #conf265={'branch':'mg265' ,'dir':'mg265'       ,
    #         'process':[
    #             #'dyellell012j_5f_LO_MLM',
    #             'dyellell012j_5f_NLO_FXFX'
    #         ],
    #}


    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", help="git branch name")
    parser.add_argument("--dirname", help="working dir name")
    parser.add_argument('--proc', nargs='+')
    args = parser.parse_args()

    if not args.branch : print "--branch <branch>"
    if not args.dirname : print "--dirname <dirname>"
    if not args.proc : print "--proc <proc>"

    conf = {'branch' : args.branch,
            'process' : args.proc,
            'dir' : args.dirname
        }
    submit_by_dictionary(conf)
    #submit_by_dictionary(conf260)
    #submit_by_dictionary(conf261)
    #submit_by_dictionary(conf265)

