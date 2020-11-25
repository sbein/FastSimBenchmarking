# FastSimBenchmarking

This repo facilitates the measurement of performance (MEM and CPU) benchmarks for FastSim. The idea is to run standard fast chain jobs, e.g., ttbar with PU X for a given CMSSW version, with the customization module --customise=Validation/Performance/TimeMemoryInfo.py, wrapped in a call of igprof (ignonimous profiler), and then extract reported quantities from the output. 

```
git clone https://github.com/sbein/FastSimBenchmarking
cd FastSimBenchmarking/
mkdir jobs
mkdir greplogs
mkdir derivedroots
```

### Example with a single interactive job

```
export SCRAM_ARCH=slc7_amd64_gcc700
scram project CMSSW_10_5_0
cd CMSSW_10_5_0/src
eval `scramv1 runtime -sh`
cd ../../

cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --datamix PreMix --conditions auto:run2_mc --pileup_input file:../PileUpFilesC10/SingleNuE10_cfi_GEN_SIM_RECOBEFMIX_DIGI_PU140.root --fast -n 100 --era Run2_2016 --eventcontent FEVTDEBUGHLT  --procModifiers premix_stage2 --relval 100000,1000 -s GEN,SIM,RECOBEFMIX,DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,L1Reco,RECO --datatier GEN-SIM-DIGI-RECO --beamspot Realistic50ns13TeVCollision --python_filename=config_CMSSW_10_5_0_fast.py --no_exec --customise=Validation/Performance/TimeMemoryInfo.py

igprof -d -mp -o igprofMEM_step3_config_CMSSW_10_5_0_fast.mp -D 100evts cmsRun config_CMSSW_10_5_0_fast.py >& igprofMEM_step3_config_CMSSW_10_5_0_fast.log 
```

The last command produces two output files containing information about the task and its timing. Note the root file itself is suppressed, but the output logs are kept, which contain the relevant info. They can be grep'd for the important information using

```
grep "^MemoryCheck\|^TimeEvent>" igprofMEM_step3_config_CMSSW_10_5_0_fast.log > greplogs/CMSSW_10_5_0_fast_timememory.txt
grep "^MemoryCheck\|^TimeEvent>" igprofMEM_step3_config_CMSSW_10_5_0_fast.log  | awk -f awkscripts/getTimeMemSummary.awk >> greplogs/CMSSW_10_5_0_fast_timememory.txt
echo "now large grep:"
grep "TimeReport" igprofMEM_step3_config_CMSSW_10_5_0_fast.log > greplogs/CMSSW_10_5_0_fast_timereport.txt
grep "Throughput" igprofMEM_step3_config_CMSSW_10_5_0_fast.log >> greplogs/CMSSW_10_5_0_fast_timereport.txt
```

### Example with a bunch of different production runs which then plots the through put vs CMSSW release
```
python scripts/submit_performance.py --slv sl7 --isfast True
```
This script allows you to select which CMSSW versions to create project areas for and then carries out ttbar production samples for each. By default it actually runs jobs interactively but in parallel. If this creates a load on the system, it is advisable to do this in series, by setting ```parallelizejobs``` to False. With a bit of care, different pile-up scenarios can also be selected, and the option to run with FullSim can also be specified. 

#### make TH1s from time report logs, store with canvases in ```derivedroots/```
```
python scripts/mkhists_timereport.py
```

#### just plot canvases
```
python scripts/plot_Throughput.py
```

