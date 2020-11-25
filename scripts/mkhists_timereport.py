import os, sys
from glob import glob
from ROOT import *
from shared_utils import *
gROOT.SetBatch(1)


try: fastfull = sys.argv[1]
except: fastfull = 'fast'

    
fnew = TFile('derivedroots/timingplots'+fastfull+'.root','recreate')

modulesets = {}
modulenames = []

cmsswnames = []

reportlogfiles = glob('greplogs/CMSSW_*'+fastfull+'*_timereport.txt')
for reportfilename in reportlogfiles:
    cmsswv = reportfilename.split('/')[-1].split('_timereport')[0].replace('_10_','_99_').replace('_11_','_999_').replace('_',',')
    if not cmsswv in cmsswnames: cmsswnames.append(cmsswv)
    print 'evaluating ', cmsswv
    reportfile = open(reportfilename)
    reportlines = reportfile.readlines()
    reportfile.close()
    for line in reportlines:
        if '>' in line: continue
        if '-----' in line: continue
        if 'efficiency' in line: continue        
        arr = line.split()
        if not (len(arr)==5 or 'Throughput' in line): 
            continue
        print 'accepting', arr
        if 'Throughput' in line:
            modulename = arr[1]
            print line
            timeperevent = 1./float(arr[2]) 
            print 'thats the number', timeperevent
        else:
            modulename = arr[4]
            timeperevent = float(arr[1])

        if not modulename in modulenames:
            modulenames.append(modulename)
            modulesets[modulename] = {}
            print 'obtained', modulename
                    
        if not cmsswv in modulesets[modulename].keys(): 
            modulesets[modulename][cmsswv] = timeperevent

cmsswnames = sorted(cmsswnames)
for key in modulesets:
    cmsswvs = sorted(modulesets[key].keys())
        

hframe = TH1F('','',len(cmsswnames),0,len(cmsswnames))
hframe.LabelsOption("v0", "X")
histoStyler(hframe, kBlack)
for modulename in modulenames:
    c1 = mkcanvas('c_'+modulename)
    h = hframe.Clone('h_'+modulename)
    xax = h.GetXaxis()
    for icms, cmsswv in enumerate(cmsswnames):
        xax.SetBinLabel(icms+1, cmsswv.replace(',999,','_11_').replace(',99,','_10_').replace(',','_').replace('_fast',''))
        if cmsswv in modulesets[modulename].keys():
            time = modulesets[modulename][cmsswv]
            h.SetBinContent(icms+1, time)
            print cmsswv, time
        else: h.SetBinContent(icms, 0)
    h.Draw('hist')
    fnew.cd()
    h.Write(h.GetName().replace(':',''))
    c1.Update()
    #
    #c1.Write()

print 'just created', fnew.GetName()
fnew.Close()
        
        
    
    


'''
TimeReport ---------- Event  Summary ---[sec]----

TimeReport ---------- Path   Summary ---[Real sec]----

TimeReport -------End-Path   Summary ---[Real sec]----

TimeReport ---------- Modules in Path: generation_step ---[Real sec]----

TimeReport ---------- Modules in Path: simulation_step ---[Real sec]----

TimeReport ---------- Modules in Path: reconstruction_befmix_step ---[Real sec]----

TimeReport ---------- Modules in Path: digitisation_step ---[Real sec]----

TimeReport ---------- Modules in Path: L1simulation_step ---[Real sec]----

TimeReport ---------- Modules in Path: digi2raw_step ---[Real sec]----

TimeReport ---------- Modules in Path: L1Reco_step ---[Real sec]----

TimeReport ---------- Modules in Path: reconstruction_step ---[Real sec]----

TimeReport ---------- Modules in Path: eventinterpretaion_step ---[Real sec]----

TimeReport ---------- Modules in Path: prevalidation_step ---[Real sec]----

TimeReport ------ Modules in End-Path: genfiltersummary_step ---[Real sec]----

TimeReport ------ Modules in End-Path: validation_step ---[Real sec]----

TimeReport ------ Modules in End-Path: dqmoffline_step ---[Real sec]----

TimeReport ------ Modules in End-Path: dqmofflineOnPAT_step ---[Real sec]----

TimeReport ---------- Module Summary ---[Real sec]----
'''
