import os, sys
from glob import glob
from ROOT import *
from shared_utils import *
#gROOT.SetBatch(1)
gStyle.SetOptStat(0)


try: fastPUfastNoPU = sys.argv[1]
except: fastPUfastNoPU = 'fastPU'

fnew=TFile('throughput.root','recreate')

colors = [1,   kBlue, kGray, kRed, kGreen, kYellow, kTeal-5, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kTeal, kOrange+2]
for color in colors[1:]:
#    colors.append(color-1)    
    colors.append(color+1)
#    colors.append(color+2)            


files = ['derivedroots/timingplotsfast.root','../Analysis/derivedroots/timingplotsfast.root']
files = files[:1]

c1 = mkcanvas('c1')
c1.SetGridx()
leg = mklegend(x1=.14, y1=.67, x2=.65, y2=.87, color=kWhite)
hists = []
arg = 'hist text'
for ifname, fname in enumerate(files):
    f =  TFile(fname)   
    f.ls()
    h = f.Get('h_Throughput')
    histoStyler(h, colors[ifname])
    h.SetLineWidth(3)
    h.GetYaxis().SetRangeUser(0,25)
    h.GetYaxis().SetTitle('1/Throughput (time/event)')
    h.SetDirectory(0)
    hists.append(h)
    hists[-1].Draw('hist text')
    arg = 'hist text same'
    leg.AddEntry(hists[-1], 't#bar{t} Fast '+fname.split('/')[-1].replace('.root',''))
    f.Close()
leg.Draw()
c1.Update()
pause()    
fnew.cd()
c1.Write()

print 'just created', fnew.GetName()

fnew.Close()
