import os, sys
from glob import glob


PU = '140'

#cmsDriver.py SingleNuE10_cfi.py --pileup_input file:MinBias_13TeV_pythia8_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX.root --mc --eventcontent PREMIX --fast --pileup AVE_25_BX_25ns  --conditions auto:run2_mc -n 500 --era Run2_2016 --eventcontent PREMIX --relval 9000,50 --step GEN,SIM,RECOBEFMIX,DIGI,L1,DIGI2RAW --datatier GEN-SIM-DIGI-RAW --beamspot Realistic25ns13TeV2016Collision 

'''
nohup python tools/submit_performance.py --slv sl6 --isfast True
nohup python tools/submit_performance.py --slv sl6 --isfast False
nohup python tools/submit_performance.py --slv sl7 --isfast True
nohup python tools/submit_performance.py --slv sl7 --isfast False
'''
##tricky thing to not actually rerun:
#grep Throughput jobs/*.sh | grep -o '.\{0,0\}grep.\{0,500\}'


test = True
condormode = False

cwd = os.getcwd()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-cmsswv", "--cmsswv", type=str,default='CMSSW_10_3_0',help="analyzer")
parser.add_argument("-slv", "--slv", type=str,default='sl7',help="sl6")
parser.add_argument("-isfast", "--isfast", type=str,default='True')
args = parser.parse_args()
isfast = args.isfast=='True'
slv = args.slv
cmsswv = args.cmsswv
verbosity = bool(args.verbosity==True)
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])

'''
cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --datamix PreMix --conditions auto:run2_mc --pileup_input file:../PileUpFilesC10/SingleNuE10_cfi_GEN_SIM_RECOBEFMIX_DIGI_PU.root.root --fast  -n 100 --era Run2_2016 --eventcontent FEVTDEBUGHLT,DQM --procModifiers premix_stage2 --relval 100000,500 -s GEN,SIM,RECOBEFMIX,DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,L1Reco,RECO,VALIDATION --datatier GEN-SIM-DIGI-RECO,DQMIO --beamspot Realistic25ns13TeV2016Collision 
'''

if isfast:
    fastfull = 'fast'
    cmsDriverCommand = 'cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --datamix PreMix --conditions auto:run2_mc --pileup_input file:../PileUpFilesC10/SingleNuE10_cfi_GEN_SIM_RECOBEFMIX_DIGI_PU'+PU+'.root --fast -n 100 --era Run2_2016 --eventcontent FEVTDEBUGHLT  --procModifiers premix_stage2 --relval 100000,1000 -s GEN,SIM,RECOBEFMIX,DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,L1Reco,RECO --datatier GEN-SIM-DIGI-RECO --beamspot Realistic50ns13TeVCollision --python_filename=config_CMSSWV_fast.py --no_exec --customise=Validation/Performance/TimeMemoryInfo.py' #
else:
    fastfull = 'full'
    cmsDriverCommand = 'cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --conditions auto:run2_mc -n 100 --era Run2_2016 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,L1Reco,RECO --datatier GEN-SIM-DIGI-RECO --beamspot Realistic50ns13TeVCollision --python_filename=config_CMSSWV_full.py --no_exec  --customise=Validation/Performance/TimeMemoryInfo.py' #
    

if slv=='sl7': 
    scramarch = 'slc7_amd64_gcc700'
    projectversion = [['CMSSW_10_4_0','slc7_amd64_gcc700'],\
                      ['CMSSW_10_5_0','slc7_amd64_gcc700'],\
                      ['CMSSW_10_6_0','slc7_amd64_gcc700'],\
                      ['CMSSW_11_1_0_pre4','slc7_amd64_gcc900'],\
                      ['CMSSW_11_1_0_pre2','slc7_amd64_gcc900']]

if slv=='sl6':
    projectversion = [
                      ['CMSSW_9_0_0','slc6_amd64_gcc630'],\
                      ['CMSSW_9_1_0','slc6_amd64_gcc630'],\
                      ['CMSSW_9_2_0','slc6_amd64_gcc630'],\
                      ['CMSSW_9_3_0','slc6_amd64_gcc630'],\
                      ['CMSSW_9_4_0','slc6_amd64_gcc630']]

'''
['CMSSW_7_0_0','slc6_amd64_gcc530'],\
                      ['CMSSW_7_1_0','slc6_amd64_gcc530'],\
                      ['CMSSW_7_2_0','slc6_amd64_gcc530'],\
                      ['CMSSW_7_3_0','slc6_amd64_gcc530'],\
                      ['CMSSW_7_4_0','slc6_amd64_gcc530'],\
                      ['CMSSW_8_0_0','slc6_amd64_gcc530'],\
                      ['CMSSW_8_1_0','slc6_amd64_gcc530'],\
                      ['CMSSW_8_2_0','slc6_amd64_gcc530'],\
                      ['CMSSW_8_3_0','slc6_amd64_gcc530'],\
'''

projectversion.reverse()
def main():
    for pv in projectversion:
        cmsswv, scramarch = pv
        jobname = cmsswv
        squishedargs = '-'.join(moreargs.split())
        jfilename = 'jobs/runsequence_'+cmsswv+squishedargs+'.sh'
        print 'jobname', jobname
        fjob = open(jfilename,'w')

        script = jobscript.replace('CWD',cwd).replace('CMSSWV',cmsswv).replace('SCRAMARCH',scramarch).replace('MOREARGS',moreargs)
        script = script.replace('FASTFULL',fastfull)
        if 'CMSSW_11' in cmsswv: script = script.replace('standardDQM','standardDQMFS')
        fjob.write(script)
        fjob.close()
        if (False and condormode):
            os.chdir('logs')
            command = 'condor_qsub -cwd '+jobname+'.sh &'                
            print 'command'
            print command
            if not test: os.system(command)
            os.chdir('..')
        else:
            command = 'bash '+jfilename+' > jobs/log'+cmsswv+moreargs+'.txt &'
            print 'command'
            print command            
            if not test: os.system(command)



jobscript='''
export SCRAM_ARCH=SCRAMARCH
scram project CMSSWV
cd CMSSWV/src
eval `scramv1 runtime -sh`

cd ../../

echo starting

'''
jobscript+=cmsDriverCommand

jobscript+='''

echo mem

igprof -d -mp -o igprofMEM_step3_config_CMSSWV_FASTFULL.mp -D 100evts cmsRun config_CMSSWV_FASTFULL.py >& igprofMEM_step3_config_CMSSWV_FASTFULL.log 

#echo cpu
#igprof -d -pp -z -o igprofCPU_step3_config_CMSSWV_FASTFULL.gz -t cmsRun cmsRun config_CMSSWV_FASTFULL.py >& igprofCPU_step3_config_CMSSWV_FASTFULL.log 

echo "now large grep:"
grep "^MemoryCheck\|^TimeEvent>" igprofMEM_step3_config_CMSSWV_FASTFULL.log > greplogs/CMSSWV_FASTFULL_timememory.txt
echo "now summary:"
grep "^MemoryCheck\|^TimeEvent>" igprofMEM_step3_config_CMSSWV_FASTFULL.log  | awk -f awkscripts/getTimeMemSummary.awk >> greplogs/CMSSWV_FASTFULL_timememory.txt
echo "now large grep:"
grep "TimeReport" igprofMEM_step3_config_CMSSWV_FASTFULL.log > greplogs/CMSSWV_FASTFULL_timereport.txt
grep "Throughput" igprofMEM_step3_config_CMSSWV_FASTFULL.log >> greplogs/CMSSWV_FASTFULL_timereport.txt
'''

main()
