import ROOT
from array import array
import pickle
import os,sys
from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_80X_postProcessed import *
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_postProcessed import *
from math import *
from selection_helpers import *
from helpers import *

postProcessing_directory = "postProcessed_80X_v12/dilepTiny/"
small = False

def makeCut(cut_value,cut_string):
  if len(cut_value)>1 and cut_value[1]>=0:
    cut = "("+cut_string+">"+str(cut_value[0])+"&&"\
            +cut_string+"<="+str(cut_value[1])+" )"
    name = "_".join([cut_string,str(cut_value[0]),cut_value[1]])
    return cut,name
  else:
    cut = "("+cut_string+">"+str(cut_value[0])+")"
    name = "".join([cut_string,str(cut_value[0]),"p"])
    return cut,name

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dl_mt2ll", dest="dl_mt2ll",     default="0,-1", type="string", action="store", help="Which SR")
parser.add_option("--dl_mt2bb", dest="dl_mt2bb",     default="0,-1", type="string", action="store", help="Which SR")
parser.add_option("--dl_mt2blbl", dest="dl_mt2blbl", default="0,-1", type="string", action="store", help="Which SR")
parser.add_option("--metMeff", dest="metMeff",       default="0,-1", type="string", action="store", help="Which SR")
parser.add_option("--metSig", dest="metSig",         default="0,-1", type="string", action="store", help="Which SR")
parser.add_option("--met"   , dest="met"  ,          default="0,-1", type="string", action="store", help="Which SR")
(options, args) = parser.parse_args()
#mt2ll_cuts   = eval("["+options.dl_mt2ll+"]")
#mt2bb_cuts   = eval("["+options.dl_mt2bb+"]")
#mt2blbl_cuts = eval("["+options.dl_mt2blbl+"]")
#met_cuts = eval("["+options.met+"]")
#metSig_cuts = eval("["+options.metSig+"]")
#metMeff_cuts = eval("["+options.metMeff+"]")

mt2ll_cut   = eval("("+options.dl_mt2ll+")")
mt2bb_cut   = eval("("+options.dl_mt2bb+")")
mt2blbl_cut = eval("("+options.dl_mt2blbl+")")
met_cut     = eval("("+options.met+")")
metSig_cut  = eval("("+options.metSig+")")
metMeff_cut = eval("("+options.metMeff+")")

metmeff_str = '(met_pt/((Sum$(JetGood_pt)*(Iteration$<2))+(l1_pt+l2_pt)+met_pt))'
lep_b_var = '(JetGood_pt[0]*(JetGood_pt>30&&abs(JetGood_eta)<2.4&&JetGood_id&&JetGood_btagCSV>0.605)+LepGood_pt[0])'

mc_samples = [DY_HT_LO,diBoson,triBoson,TTZ_LO, TTW, Top ]
T2tt_700_50.color = ROOT.kRed
T2tt_650_300.color = ROOT.kGreen
T2tt_450_250.color = ROOT.kBlue
signal_samples = [T2tt_700_50, T2tt_650_300, T2tt_450_250]
data_samples = [DoubleMuon_Run2016BCD_backup , DoubleEG_Run2016BCD_backup , MuonEG_Run2016BCD_backup]

if small:
  for sample in mc_samples + data_samples + signal_samples:
      sample.reduceFiles(to = 1)

plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{jet}','logy':'True' , 'var':'nJetGood',        'bin_set':(False,25),'varname':'nJet30', 'binlabel':1,  'bin':(15,0,15)},\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{b-tag}','logy':'True' , 'var':'nBTag',         'bin_set':(False,25),'varname':'nBTag',  'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
#{'ndiv':True,'yaxis':'Events /','xaxis':'lepton1+b1 (GeV)','logy':'True' , 'var':lep_b_var,'bin_set':(False,25),'varname':'lepton1_b1',  'binlabel':40,  'bin':(25,0,1000) },\
{'ndiv':True,'yaxis':'Events /','xaxis':'leptonPt[0] (GeV)','logy':'True' , 'var':'LepGood_pt[0]','bin_set':(False,25),'varname':'LeadingleptonPt',  'binlabel':40,  'bin':(25,0,1000) },\
{'ndiv':True,'yaxis':'Events /','xaxis':'H_{T} (GeV)','logy':'True' , 'var':'ht',         'bin_set':(False,25),'varname':'ht',  'binlabel':100,  'bin':(26,0,2600) },\
{'ndiv':True,'yaxis':'Events / ','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',  'bin_set':(False,25),'varname':'met',    'binlabel':50,  'bin':(28,0,1400)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'MT_{2}^{ll} (GeV)','logy':'True' , 'var':'dl_mt2ll',  'bin_set':(False,25),'varname':'dl_mt2ll',    'binlabel':25,  'bin':(20,0,500)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'MT_{2}^{blbl} (GeV)','logy':'True' , 'var':'dl_mt2blbl',  'bin_set':(False,25),'varname':'dl_mt2blbl',    'binlabel':25,  'bin':(20,0,500)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'MT_{2}^{bb} (GeV)','logy':'True' , 'var':'dl_mt2bb',  'bin_set':(False,25),'varname':'dl_mt2bb',    'binlabel':25,  'bin':(20,0,500)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'#slash{E}_{T}/#sqrt{H_{T}} (GeV^{1/2})','logy':'True' , 'var':'metSig',  'bin_set':(False,25),'varname':'metSig',    'binlabel':100,  'bin':(30,0,30)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#slash{E}_{T} / m_{eff} (GeV))','logy':'True' , 'var':metmeff_str,  'bin_set':(False,25),'varname':'metOvmeff',    'binlabel':1,  'bin':(10,0,1)},\
  ]

#plots = [plots[2]]

print "====== "
presel = mc_sel_string
sig_presel = test_sel_string
data_presel = mc_sel_string


#for metMeff_cut in metMeff_cuts:
#  for met_cut in met_cuts:
#    for metSig_cut in metSig_cuts:
#      for mt2blbl_cut in mt2blbl_cuts:
#        for mt2bb_cut in mt2bb_cuts:
#          for mt2ll_cut in mt2ll_cuts:

cut_SR = "&&".join([makeCut(mt2ll_cut , "dl_mt2ll")[0] , makeCut(mt2bb_cut , "dl_mt2bb")[0] , makeCut(mt2blbl_cut , "dl_mt2blbl")[0] , makeCut(met_cut , "met_pt")[0], makeCut(metSig_cut , "metSig")[0], makeCut(metMeff_cut , metmeff_str)[0]]) 
name_SR = "_".join([makeCut(mt2ll_cut , "dl_mt2ll")[1] , makeCut(mt2bb_cut , "dl_mt2bb")[1] , makeCut(mt2blbl_cut , "dl_mt2blbl")[1] ,makeCut(met_cut , "met_pt")[1], makeCut(metSig_cut , "metSig")[1],makeCut(metMeff_cut , "metMeff")[1]]) 

print name_SR

path = "/afs/hephy.at/user/e/easilar/www/data/80X_v12_5/"+selectionString["name"]+"/"+name_SR+"/"
if not os.path.exists(path):
  os.makedirs(path)

for p in plots:
  for bkg in mc_samples:
    p[bkg.name] = getPlotFromChain(bkg.chain, p['var'], p['bin'], cutString = "&&".join([presel,cut_SR]), weight = mc_weight_string , binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"])
  for sig in signal_samples:
    p[sig.name] = getPlotFromChain(sig.chain, p['var'], p['bin'], cutString = "&&".join([sig_presel,cut_SR]), weight = sig_weight_string , binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"]) 
  for data in data_samples:
    p[data.name.split("_")[0]] = getPlotFromChain(data.chain, p['var'], p['bin'], cutString = "&&".join([data_presel,cut_SR]), weight = "(1)" , binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"])

for p in plots:
  print p['xaxis']
  cb = ROOT.TCanvas("cb","cb",564,232,600,600)
  cb.SetHighLightColor(2)
  cb.Range(0,0,1,1)
  cb.SetFillColor(0)
  cb.SetBorderMode(0)
  cb.SetBorderSize(2)
  cb.SetTickx(1)
  cb.SetTicky(1)
  cb.SetLeftMargin(0.18)
  cb.SetRightMargin(0.04)
  cb.SetTopMargin(0.05)
  cb.SetBottomMargin(0.13)
  cb.SetFrameFillStyle(0)
  cb.SetFrameBorderMode(0)
  cb.SetFrameFillStyle(0)
  cb.SetFrameBorderMode(0)
  cb.cd()
  
  #cb.SetRightMargin(3)
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.05)
  latex.SetTextAlign(11)
  
  leg = ROOT.TLegend(0.65,0.5,0.93,0.925)
  leg.SetBorderSize(1)
  leg_sig = ROOT.TLegend(0.3,0.8,0.6,0.925)
  leg_sig.SetBorderSize(1)
  Pad1 = ROOT.TPad("Pad1", "Pad1", 0,0.31,1,1)
  Pad1.Draw()
  Pad1.cd()
  #Pad1.Range(-0.7248462,-1.30103,3.302077,3.159352)
  Pad1.SetFillColor(0)
  Pad1.SetBorderMode(0)
  Pad1.SetBorderSize(2)
  Pad1.SetLogy()
  Pad1.SetTickx(1)
  Pad1.SetTicky(1)
  Pad1.SetLeftMargin(0.18)
  Pad1.SetRightMargin(0.04)
  Pad1.SetTopMargin(0.055)
  Pad1.SetBottomMargin(0)
  Pad1.SetFrameFillStyle(0)
  Pad1.SetFrameBorderMode(0)
  Pad1.SetFrameFillStyle(0)
  Pad1.SetFrameBorderMode(0)
  Pad1.SetLogy()
  #Pad1.Draw()
  #Pad1.cd()
  #ROOT.gStyle.SetHistMinimumZero()
  ROOT.gStyle.SetErrorX(.5)
  h_Stack = ROOT.THStack('h_Stack','h_Stack')
  for bkg in mc_samples:
    color = bkg.color
    histo = p[bkg.name]
    histo.SetFillColor(color)
    histo.SetLineColor(ROOT.kBlack)
    histo.SetLineWidth(1)
    Set_axis_pad1(histo)
    #histo.GetXaxis().SetTitle(p['xaxis'])
    #histo.SetTitle("")
    #histo.GetYaxis().SetTitleSize(2)
    if p['ndiv']:
       histo.GetXaxis().SetNdivisions(505)
       #histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
       histo.GetYaxis().SetTitle(p['yaxis'])
    if not p['ndiv']:
       histo.GetYaxis().SetTitle(p['yaxis'])
    #leg.AddEntry(histo, bkg['tex'],"f")
    h_Stack.Add(histo)
    del histo
  #h_Stack.Draw("Bar")
  
  if p["bin_set"][0]: stack_hist=ROOT.TH1F("stack_hist","stack_hist", p['bin'][0],p['bin'][1]) 
  else: stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
  stack_hist.Merge(h_Stack.GetHists())

  max_bin = stack_hist.GetMaximum()*10000

  h_Stack.SetMaximum(max_bin)
  #h_Stack.SetMinimum(0.000000001)
  h_Stack.SetMinimum(0.11)
  
  color = ROOT.kBlack
  for i,data in enumerate(data_samples):
    #print p, data.name
    if i==0: h_data = p[data.name.split("_")[0]]
    else : h_data.Add(p[data.name.split("_")[0]])
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.1)
    h_data.SetLineColor(color)
    h_data.GetXaxis().SetTitle(p['xaxis'])
    h_data.SetTitle("")
    #h_data.GetYaxis().SetTitleSize(0.05)
    #h_data.GetYaxis().SetLabelSize(0.05)
    Set_axis_pad1(h_data)
    h_data.Draw("E1")
    h_data.SetMaximum(max_bin)
    h_data.SetMinimum(0.11)
  h_Stack.Draw("HistoSame")
  for sig in signal_samples:
    h_sig = p[sig.name]
    if presel or a_MB:
      h_sig.Scale(1)
    h_sig.SetLineColor(sig.color)
    h_sig.SetLineWidth(3)
    h_sig.SetTitle("")
    h_sig.Draw("HistoSame")
    leg_sig.AddEntry(h_sig, sig.name,"l")
    del h_sig
  h_data.Draw("E1 Same")
  if p['ndiv']:
    h_data.GetXaxis().SetNdivisions(505)
    #h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+' GeV')
    h_data.GetYaxis().SetTitle(p['yaxis'])
  if not p['ndiv']:
    h_data.GetYaxis().SetTitle(p['yaxis'])
  #print "Integral of BKG:" , stack_hist.Integral()
  #print "Integral of BKG over 200:" , stack_hist.Integral(20,100)
  #print "Integral of DATA:" , h_data.Integral()

  leg.AddEntry(h_data, "Data","PL")
  for bkg in reversed(mc_samples):
    color = bkg.color
    histo = p[bkg.name]
    histo.SetFillColor(color)
    histo.SetLineColor(ROOT.kBlack)
    histo.SetLineWidth(1)
    leg.AddEntry(histo, bkg.name,"f")

  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.Draw()
  leg_sig.SetFillColor(0)
  leg_sig.SetLineColor(0)
  leg_sig.Draw()
  Draw_CMS_header()
  Pad1.RedrawAxis()
  cb.cd()
  Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0, 1, 0.31)
  Pad2.Draw()
  Pad2.cd()
  #Pad2.Range(-0.7248462,-0.8571429,3.302077,2)
  Pad2.SetFillColor(0)
  Pad2.SetFillStyle(4000)
  Pad2.SetBorderMode(0)
  Pad2.SetBorderSize(2)
  Pad2.SetTickx(1)
  Pad2.SetTicky(1)
  Pad2.SetLeftMargin(0.18)
  Pad2.SetRightMargin(0.04)
  Pad2.SetTopMargin(0)
  Pad2.SetBottomMargin(0.3)
  Pad2.SetFrameFillStyle(0)
  Pad2.SetFrameBorderMode(0)
  Pad2.SetFrameFillStyle(0)
  Pad2.SetFrameBorderMode(0)
  if p["bin_set"][0] : Func = ROOT.TF1('Func',"[0]",p['bin'][1][0],p['bin'][1][-1])
  else: Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
  Func.SetParameter(0,1)
  Func.SetLineColor(58)
  Func.SetLineWidth(2)
  h_ratio = h_data.Clone('h_ratio')
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(stack_hist)
  rmax = 2
  for b in xrange(1,h_ratio.GetNbinsX()+1):
    if h_ratio.GetBinContent(b) == 0: continue
    rmax = max([ rmax, h_ratio.GetBinContent(b) + 2*h_ratio.GetBinError(b) ])
  print rmax
  h_ratio.SetMinimum(0.01)
  #h_ratio.SetMaximum(min(rmax,4.99))
  h_ratio.SetMaximum(min(rmax,1.9))
  h_ratio.SetMarkerStyle(20)
  h_ratio.SetMarkerSize(1.1)
  h_ratio.SetMarkerColor(ROOT.kBlack)
  h_ratio.SetTitle("")
  Set_axis_pad2(h_ratio)
  h_ratio.GetYaxis().SetTitle("Data/Pred. ")
  h_ratio.GetXaxis().SetTitle(p['xaxis'])
  h_ratio.GetYaxis().SetNdivisions(505)
  h_ratio.Draw("E1")
  Func.Draw("same")
  h_ratio.Draw("E1 Same")
  cb.Draw()
  cb.SaveAs(path+p['varname']+'.png')
  cb.SaveAs(path+p['varname']+'.pdf')
  cb.SaveAs(path+p['varname']+'.root')
  cb.Clear()
  del h_Stack

