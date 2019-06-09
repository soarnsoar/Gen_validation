import os
import socket
import subprocess
import argparse
import time



class MG_gridpackGEN():


    def __init__(self,branch,dirname):

        self.gendirname=dirname
        self.gitbranch=branch
        self.gengit='git@github.com:cms-sw/genproductions.git'
        self.MGGENDIR=None
        self.card_dir=os.getcwd()+'/mycard'
        self.curdir=os.getcwd()
        #setup vars#
        self.DIR_FLAG='bin/MadGraph5_aMCatNLO/JHCHOI_FLAGS/'
        self.wait_sec_git=10
        self.HOSTNAME=socket.gethostname()

            
        
    def setup_genproductions(self):

        ##(1)check whether the setup is done##
        #if setup never tried
        #if setup is running
        #if setup is done
        self.check_whther_the_setup_is_done()




        ##(2)set up using git
        self.setup_using_git()

        #chdir to MGwordir

        self.MGGENDIR=self.gendirname+'/bin/MadGraph5_aMCatNLO'
        print '[chdir]'+self.MGGENDIR
        os.chdir(self.MGGENDIR)

        ##(2-1) copy carddir
        os.system('cp -r '+self.card_dir+' .')

        ##(3)add runtime calc line
        command='git clone git@github.com:soarnsoar/python_tool.git'
        print command
        os.system(command)
        command='python python_tool/add_runtime.py submit_condor_gridpack_generation.sh'
        print command
        os.system(command)
        command='python python_tool/add_runtime.py submit_cmsconnect_gridpack_generation.sh'
        print command
        os.system(command)
        
        ##(4)modify SCRAM_ARCH if needed
        if 'lxplus7' in self.HOSTNAME:

            command= 'find . -name "gridpack_generation.sh" | xargs perl -pi -e s/slc6/slc7/g'
            print command
            os.system(command)
        

        ##(5)install some Genval tools
        command='git clone git@github.com:soarnsoar/Gen_validation.git'
        os.system(command)
        os.chdir(self.curdir)
    ## sub module of setup_genproductions() ##
    def check_whther_the_setup_is_done(self):
        #if genproductions exist
        if os.path.isfile(self.gendirname):
            FLAG=self.gendirname+"/"+self.DIR_FLAG+'/SETUP_DONE'
            done=os.path.isfile(FLAG)
            if done: 
                return
            else:
                ##The setup is not completed yet##
                #wait until done
                while 1 :
                    print "[Setup] Git repository is not setup yet, wait "+str(self.wait_sec_git)+" sec"
                    time.sleep(self.wait_sec_git)
                    if os.path.isfile(FLAG):break
    
    def setup_using_git(self):
        command= "git clone "+self.gengit+" -b "+self.gitbranch+' '+self.gendirname
        print "---"+command+"---"
        os.system(command)
        os.system('mkdir -p '+self.gendirname+'/'+self.DIR_FLAG)
        os.system('touch '+self.gendirname+"/"+self.DIR_FLAG+'/SETUP_DONE')
        

    def make_submit_script(self,process_name):
 
        ##(1) set up submission command
        #if lxplus -> source submit_condor~~
        #if cmsconnect -> nohup ./submit_cmsconnect_~~~
        


        script ='submit_condor_gridpack_generation.sh'
        execute ='source'
        ##if cms connect##
        commnad=execute+' '+script+' '+process_name+' '+self.card_dir.split('/')[-1]+'/'+process_name+' &> '+process_name+'.debug&'
        if 'login.uscms.org' in self.HOSTNAME:
            script  = 'submit_cmsconnect_gridpack_generation.sh'
            execute = 'nohup'
            command=execute+' ./'+script+' '+process_name+' '+self.card_dir.split('/')[-1]+'/'+process_name+' > '+process_name+'.debug 2>&1 &'

        ##(2) make submission script
        #contents : 
        # go to MGGENworkdir
        # run submission
        # run standalone test
        # if done -> send an email
        scriptname='run__'+self.gitbranch+"__"+self.gendirname+"__"+process_name+'.sh'
        f=open(scriptname,'w')
        f.write('pushd '+self.MGGENDIR+'\n')
        f.write('rm -rf '+process_name+'\n')
        f.write('rm '+process_name+'log\n')
        f.write('rm '+process_name+'debug\n')
        f.write('rm '+process_name+'_codegen.sh\n')
        f.write(command+'\n')
        f.write('popd\n')
        f.close()
        print "---DONE---"
        print 'source '+scriptname
        






def submit_by_dictionary(conf):
    myMG=MG_gridpackGEN(conf['branch'],conf['dir'])
    
    myMG.setup_genproductions()

    for p in conf['process']:

        print p
        myMG.make_submit_script(p)

    

if __name__ == "__main__":
    ##Submit example
    # python setup_gridpack_generation.py --branch master --dirname mg260_master --proc dy01234j_LO_MLM_blahblah
    
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
