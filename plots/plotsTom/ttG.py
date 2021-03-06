#!/usr/bin/env python
''' Analysis script for TTG selection (g bbllnunu or g bbjjlnu)
'''
#
# Standard imports and batch mode
#
import ROOT
ROOT.gROOT.SetBatch(True)

from math import sqrt, cos, sin, pi
from RootTools.core.standard import *
from StopsDilepton.tools.user import plot_directory
from StopsDilepton.tools.helpers import deltaPhi
from StopsDilepton.tools.objectSelection import getFilterCut

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--subtract',       action='store_true', default=False,       help='subtract residual backgrounds?')
argParser.add_argument('--add2015',        action='store_true', default=False,       help='add 2015?')
argParser.add_argument('--plot_directory', action='store',      default='TTG')
argParser.add_argument('--selection',      action='store',      default=None)
argParser.add_argument('--isChild',        action='store_true', default=False)
argParser.add_argument('--dryRun',         action='store_true', default=False,       help='do not launch subjobs')
args = argParser.parse_args()
if args.subtract: args.plot_directory += "_subtracted"

#
# Logger
#
import StopsDilepton.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

#
# Selections (two leptons with pt > 20 GeV, photon)
#
from StopsDilepton.tools.objectSelection import multiIsoLepString
multiIsoWP = multiIsoLepString('VT','VT', ('l1_index','l2_index'))
def getLeptonString(nMu, nE, multiIso=False, is74x=False):
  leptonString = "nGoodMuons==" + str(nMu) + "&&nGoodElectrons==" + str(nE) + "&&l1_pt>25"
  if multiIso and is74x: leptonString += "&&l1_index>=0&&l1_index<1000&&l2_index>=0&&l2_index<1000&&"+multiIsoWP
  elif multiIso:         leptonString += "&&l1_mIsoWP>4&&l2_mIsoWP>4"
  return leptonString


jetSelection    = "(Sum$(JetGood_pt>30&&abs(JetGood_eta)<2.4&&JetGood_id))>="
bJetSelectionM  = "(Sum$(JetGood_pt>30&&abs(JetGood_eta)<2.4&&JetGood_id&&JetGood_btagCSV>0.800))>="
bJetSelectionL  = "(Sum$(JetGood_pt>30&&abs(JetGood_eta)<2.4&&JetGood_id&&JetGood_btagCSV>0.460))>="

#
# Cuts to iterate over
#
cuts = [
    ("njet2",             jetSelection+"2"),
    ("multiIsoWP",        "(1)"),                       # implemented below
    ("photon30",          "(1)"),
    ("llgNoZ",            "(1)"),			# Cut implemented in lepton selection
    ("gJetdR",            "(1)"),			# Implenented in otherSelections() method
    ("gLepdR",            "(1)"),			# Implemented in otherSelections() method
    ("btagL",             bJetSelectionL+"1"),
    ("btagM",             bJetSelectionM+"1"),
    ("mll20",             "dl_mass>20"),
    ("met80",             "met_pt_photonEstimated>80"),
    ("metSig5",           "metSig_photonEstimated>5"),
    ("dPhiJet0-dPhiJet1", "cos(met_phi_photonEstimated-JetGood_phi[0])<0.8&&cos(met_phi_photonEstimated-JetGood_phi[1])<cos(0.25)"),
  ]


#
# Construct prefixes and selectionstring and filter on possible cut combinations
#
import itertools
selectionStrings = {}
for i_comb in reversed( range( len(cuts)+1 ) ):
    for comb in itertools.combinations( cuts, i_comb ):
        presel = [] 
        presel.extend( comb )
        selection = '-'.join([p[0] for p in presel])
        if selection.count("btag") > 1:    continue
        if selection.count("photon") != 1: continue
        if selection.count("njet") != 1:   continue
        if selection.count("dPhiJet0-dPhiJet1") and not selection.count("metSig5"):  continue
        if selection.count("metSig5")           and not selection.count("met80"):    continue
        if selection.count("met80")             and not selection.count("mll20"):    continue
        if selection.count("mll20")             and not selection.count("btag"):     continue
        if selection.count("mll20")             and not selection.count("llgNoZ"):   continue
        if selection.count("mll20")             and not selection.count("gJetdR"):   continue
        if selection.count("mll20")             and not selection.count("gLepdR"):   continue
        if not selection in ["njet2-photon30-llgNoZ-gJetdR-gLepdR-btagM-mll20",
                             "njet2-photon30-llgNoZ-gJetdR-gLepdR-btagM-mll20-met80-metSig5-dPhiJet0-dPhiJet1",
                             "njet2-photon30",
                             "njet2-photon30-gJetdR-gLepdR-btagM",
                             "njet2-photon30-llgNoZ-gJetdR-gLepdR-btagM-mll20-met80",
                             "njet2-photon30-llgNoZ",
                             "njet2-photon30-llgNoZ-gJetdR-gLepdR-btagM"]: continue

        selectionStrings[selection] = "&&".join( [p[1] for p in presel])

#
# If this is the mother process, launch the childs and exit (I know, this could potententially be dangereous if the --isChild and --selection commands are not given...)
#
if not args.isChild and args.selection is None:
  import os
  os.system("mkdir -p log")
  for selection in selectionStrings:
    command = "./ttG.py --selection=" + selection + (" --subtract" if args.subtract else "") + (" --add2015" if args.add2015 else "")
    logfile = "log/" + selection + ".log"
    logger.info("Launching " + selection + " on cream02 with child command: " + command)
    if not args.dryRun: os.system("qsub -v command=\"" + command + " --isChild\" -q localgrid@cream02 -o " + logfile + " -e " + logfile + " -l walltime=03:00:00 runPlotsOnCream02.sh")
  logger.info("All jobs launched")
  exit(0)

if args.add2015:
  args.plot_directory += "_combined"

#
# Make samples, will be searched for in the postProcessing directory
#
postProcessing_directory = "postProcessed_80X_v12/dilepTiny/"
from StopsDilepton.samples.cmgTuples_Data25ns_80X_postProcessed import *
from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed import *
from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed_photonSamples import *


#
# Text on the plots
#
def drawObjects( dataMCScale, lumi_scale ):
    if args.add2015: lumi_scale += 2.16
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.95, 'CMS Preliminary'), 
      (0.45, 0.95, 'L=12.9 fb{}^{-1} (13 TeV) Scale %3.2f'% ( dataMCScale ) )
    ]
    return [tex.DrawLatex(*l) for l in lines] 


#
# Read variables and sequences
#
read_variables = ["weight/F" , "l1_eta/F" , "l1_phi/F", "l2_eta/F", "l2_phi/F", "JetGood[pt/F,eta/F,phi/F,btagCSV/F]", "dl_mass/F", "dl_eta/F", "dl_mt2ll_photonEstimated/F", "dl_mt2bb_photonEstimated/F", "dl_mt2blbl_photonEstimated/F",
                  "met_pt_photonEstimated/F", "met_phi_photonEstimated/F",
                  "metSig_photonEstimated/F", "ht/F", "nBTag/I", "nJetGood/I", "mt_photonEstimated/F", "photon_pt/F", "photon_eta/F",  "photon_phi/F", "photonJetdR/F", "photonLepdR/F"]

def photonDeltaR(data, eta, phi):
  return sqrt(deltaPhi(data.photon_phi, phi)**2 + (data.photon_eta - eta)**2)

def makeDeltaR(data):
  data.photonLep1DeltaR     = photonDeltaR(data, data.l1_eta, data.l1_phi)
  data.photonLep2DeltaR     = photonDeltaR(data, data.l2_eta, data.l2_phi)
  data.JetGood_photonDeltaR = [photonDeltaR(data, data.JetGood_eta[i], data.JetGood_phi[i]) for i in range(data.nJetGood)]

# Filter on dR jets and recalculate jet var
def filterJets(data):
  if args.selection.count("gJetdR"): data.goodJetIndices = [i for i in range(data.nJetGood) if data.JetGood_photonDeltaR[i] > 0.3]
  else:                              data.goodJetIndices = [i for i in range(data.nJetGood)]
  data.nJetGood               = len(data.goodJetIndices)
  data.ht                     = sum([data.JetGood_pt[j] for j in data.goodJetIndices])
  data.metSig_photonEstimated = data.met_pt_photonEstimated/sqrt(data.ht) if data.ht !=0 else float('nan')
  data.nBTag                  = len([j for j in data.goodJetIndices if data.JetGood_btagCSV[j] > 0.800])
  data.nBTagLoose             = len([j for j in data.goodJetIndices if data.JetGood_btagCSV[j] > 0.460])
  data.dPhiMetJet             = [cos(data.met_phi_photonEstimated - data.JetGood_phi[j]) for j in data.goodJetIndices]

# Make photonLepdR selection or re-evaluate jet selection after photonJetdR
def otherSelections(data, sample):
  data.passed = True
  if args.selection.count("gLepdR"):
    data.passed = (data.passed and data.photonLep1DeltaR > 0.3 and data.photonLep2DeltaR > 0.3)
  if args.selection.count("gJetdR"):
    if args.selection.count("njet2"):             data.passed = (data.passed and data.nJetGood > 1)
    if args.selection.count("btagL"):             data.passed = (data.passed and data.nBTagLoose > 0)
    if args.selection.count("btagM"):             data.passed = (data.passed and data.nBTag > 0)
    if args.selection.count("metSig5"):           data.passed = (data.passed and data.metSig_photonEstimated > 5)
    if args.selection.count("dPhiJet0-dPhiJet1"): data.passed = (data.passed and max(data.dPhiMetJet[0], data.dPhiMetJet[1]) < cos(0.25))

sequence = [makeDeltaR, filterJets, otherSelections]


offZ            = "&&abs(dl_mass-91.1876)>15"
offZ_dlg        = "&&abs(dlg_mass-91.1876)>15"
photonSelection = "nPhotonGood>0&&photon_eta<2.5&&photon_idCutBased>2&&photon_pt>" + args.selection.split('photon')[1].split('-')[0]

def getLeptonSelection(mode, llgCut = False):
  if   mode=="mumu": return getLeptonString(2, 0, args.selection.count("multiIsoWP")) + "&&isOS&&isMuMu" + offZ + (offZ_dlg if llgCut else "")
  elif mode=="mue":  return getLeptonString(1, 1, args.selection.count("multiIsoWP")) + "&&isOS&&isEMu"
  elif mode=="ee":   return getLeptonString(0, 2, args.selection.count("multiIsoWP")) + "&&isOS&&isEE" + offZ + (offZ_dlg if llgCut else "")

#
# Loop over channels
#
yields     = {}
allPlots   = {}
allModes   = ['mumu','mue','ee']
for index, mode in enumerate(allModes):
  yields[mode] = {}
  if mode=="mumu":
    data_sample           = DoubleMuon_Run2016BCD_backup
    data_sample.texName   = "data (2 #mu)"
  elif mode=="ee":
    data_sample           = DoubleEG_Run2016BCD_backup
    data_sample.texName   = "data (2 e)"
  elif mode=="mue":
    data_sample           = MuonEG_Run2016BCD_backup
    data_sample.texName   = "data (1 #mu, 1 e)"

  data_sample.setSelectionString([getFilterCut(isData=True), getLeptonSelection(mode, llgCut=args.selection.count('llgNoZ')), photonSelection])
  data_sample.name  = "data"
  data_sample.style = styles.errorStyle( ROOT.kBlack )
  lumi_scale        = data_sample.lumi/1000

  mc    = [TTG, ZG, DY_HT_LO, multiBoson, TTJets_Lep, singleTop, TTX]
  stack = Stack(mc, [data_sample])

  for sample in mc:
    sample.scale          = lumi_scale
    sample.style          = styles.fillStyle(sample.color)
    sample.read_variables = ['reweightBTag_SF/F','reweightDilepTrigger/F','reweightPU/F']
    sample.read_variables = ['reweightLeptonHIPSF/F','reweightDilepTriggerBackup/F','reweightLeptonSF/F','reweightBTag_SF/F','reweightPU12fb/F']
    sample.weight         = lambda data: data.reweightBTag_SF*data.reweightLeptonSF*data.reweightLeptonHIPSF*data.reweightDilepTriggerBackup*data.reweightPU12fb
    sample.setSelectionString([getFilterCut(isData=False), getLeptonSelection(mode, llgCut=args.selection.count('llgNoZ')), photonSelection])


  # For TTJets, do TTGJets overlap events removal
  TTJets_Lep.setSelectionString(["TTGJetsEventType<4", getFilterCut(isData=False), getLeptonSelection(mode, llgCut=args.selection.count('llgNoZ')), photonSelection])
  DY_HT_LO.setSelectionString(  ["TTGJetsEventType<4", getFilterCut(isData=False), getLeptonSelection(mode, llgCut=args.selection.count('llgNoZ')), photonSelection])

  # Use some defaults
  Plot.setDefaults(stack = stack, weight = (lambda data:data.weight if data.passed else 0), selectionString = selectionStrings[args.selection])
  
  plots = []

  plots.append(Plot(
    name = 'yield', texX = 'yield', texY = 'Number of Events',
    variable = Variable.fromString( "yield/F" ).addFiller(lambda data: 0.5 + index),
    binning=[3, 0, 3],
  ))

  plots.append(Plot(
    texX = 'm(ll) of leading dilepton (GeV)', texY = 'Number of Events / GeV',
    variable = Variable.fromString( "dl_mass/F" ),
    binning=[200/4,0,200],
  ))

  theDlgPlot = Plot(
    texX = 'm(ll#gamma) of leading dilepton and photon (GeV)', texY = 'Number of Events / GeV',
    variable = Variable.fromString( "dlg_mass/F" ),
    binning=Binning.fromThresholds([50,70,80,84,88,92,94,100,120,140,160,180,200,230,260,290,320,360]),
  )
  theDlgPlot.binWidth = 1
  plots.append(theDlgPlot)

  plots.append(Plot(
    texX = 'm(ll#gamma) of leading dilepton and photon (GeV)', texY = 'Number of Events / GeV',
    variable = Variable.fromString( "dlg_mass/F" ),
    name = "dlg_mass_zoomed",
    binning=[80, 50, 130],
  ))

  plots.append(Plot(
    texX = 'M_{T2}(ll) (including #gamma) (GeV)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString( "dl_mt2ll_photonEstimated/F" ),
    binning=[300/20,0,300],
  ))

  plots.append(Plot(
    texX = 'M_{T2}(bb) (including #gamma) (GeV)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString( "dl_mt2bb_photonEstimated/F" ),
    binning=[300/20,0,300],
  ))

  plots.append(Plot(
    texX = 'M_{T2}(blbl) (including #gamma) (GeV)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString( "dl_mt2blbl_photonEstimated/F" ),
    binning=[300/20,0,300],
  ))

  plots.append(Plot(
    texX = 'E_{T}^{miss} (including #gamma) (GeV)', texY = 'Number of Events / 50 GeV',
    variable = Variable.fromString( "met_pt_photonEstimated/F" ),
    binning=[300/50,0,300],
  ))

  plots.append(Plot(
    texX = 'E_{T}^{miss}/#sqrt{H_{T}} (including #gamma) (GeV^{1/2})', texY = 'Number of Events',
    variable = Variable.fromString('metSig_photonEstimated/F').addFiller(lambda data: data.met_pt_photonEstimated/sqrt(data.ht)),
    binning=[15,0,15],
  ))

  plots.append(Plot(
    texX = 'H_{T} (GeV)', texY = 'Number of Events / 30 GeV',
    variable = Variable.fromString( "ht/F" ).addFiller(lambda data: data.ht),
    binning=[510/30,90,600],
  ))

  plots.append(Plot(
    texX = 'Cos(#phi(E_{T}^{miss}, Jet[0]))', texY = 'Number of Events',
    variable = Variable.fromString('cosMetJet0phi/F').addFiller(lambda data: data.dPhiMetJet[0] if data.nJetGood > 0 else -1),
    binning = [10,-1,1], 
  ))

  plots.append(Plot(
    texX = 'Cos(#phi(E_{T}^{miss}, Jet[1]))', texY = 'Number of Events',
    variable = Variable.fromString('cosMetJet1phi/F').addFiller(lambda data: data.dPhiMetJet[1] if data.nJetGood > 1 else -1),
    binning = [10,-1,1], 
  ))

  plots.append(Plot(
    texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString('jet1pt/F').addFiller(lambda data: data.JetGood_pt[data.goodJetIndices[0]] if data.nJetGood > 0 else -1),
    binning=[500/20,30,530],
  ))

  plots.append(Plot(
    texX = 'p_{T}(2^{nd.} leading jet) (GeV)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString('jet2pt/F').addFiller(lambda data: data.JetGood_pt[data.goodJetIndices[1]] if data.nJetGood > 1 else -1),
    binning=[400/20,30,430],
  ))

  plots.append(Plot(
    texX = 'number of medium b-tags (CSVM)', texY = 'Number of Events',
    variable = Variable.fromString('nBTag/I').addFiller(lambda data: data.nBTag),
    binning=[8,0,8],
  ))

  plots.append(Plot(
    texX = 'number of loose b-tags (CSVM)', texY = 'Number of Events',
    variable = Variable.fromString('nBTagLoose/I').addFiller(lambda data: data.nBTagLoose),
    binning=[8,0,8],
  ))

  plots.append(Plot(
    texX = 'number of jets', texY = 'Number of Events',
    variable = Variable.fromString('nJetGood/I').addFiller(lambda data : data.nJetGood),
    binning=[14,0,14],
  ))

  plots.append(Plot(
    texX = '#eta(#gamma)', texY = 'Number of Events',
    variable = Variable.fromString( "photon_eta/F" ).addFiller(lambda data: abs(data.photon_eta)),
    binning=[10, 0, 2.4],
  ))

  plots.append(Plot(
    texX = 'p_{T}(#gamma)', texY = 'Number of Events / 20 GeV',
    variable = Variable.fromString( "photon_pt/F" ),
    binning=[10, 30,230],
  ))

  plots.append(Plot(
    texX = '#phi(#gamma)', texY = 'Number of Events',
    variable = Variable.fromString( "photon_phi/F" ),
    binning=[15,-pi,pi],
  ))

  plots.append(Plot(
    texX = '#Delta R(#gamma, l)', texY = 'Number of Events',
    variable = Variable.fromString( "photonLepdR/F" ),
    binning=[20, 0, 5],
  ))

  plots.append(Plot(
    texX = '#Delta R(#gamma, j)', texY = 'Number of Events',
    variable = Variable.fromString( "photonJetdR/F" ),
    binning=[20, 0, 5],
  ))

  plots.append(Plot(
    texX     = '#Delta R(#gamma, l_{1})', texY = 'Number of Events',
    variable = Variable.fromString("photonLep1DeltaR/F").addFiller(lambda data : data.photonLep1DeltaR),
    binning  = [20, 0, 5]
  ))

  plots.append(Plot(
    texX     = '#Delta R(#gamma, l_{2})', texY = 'Number of Events',
    variable = Variable.fromString("photonLep2DeltaR/F").addFiller(lambda data : data.photonLep2DeltaR),
    binning  = [20, 0, 5]
  ))

  plots.append(Plot(
    texX     = '#Delta R(#gamma, j_{1})', texY = 'Number of Events',
    variable = Variable.fromString("photonJet1DeltaR/F").addFiller(lambda data : data.JetGood_photonDeltaR[data.goodJetIndices[0]] if data.nJetGood > 0 else -1),
    name     = "photonJet1DeltaR",
    binning  = [20, 0, 5]
  ))

  plots.append(Plot(
    texX     = '#Delta R(#gamma, j_{2})', texY = 'Number of Events',
    variable = Variable.fromString("photonJet2DeltaR/F").addFiller(lambda data : data.JetGood_photonDeltaR[data.goodJetIndices[1]] if data.nJetGood > 1 else -1),
    name     = "photonJet2DeltaR",
    binning  = [20, 0, 5]
  ))

  plotting.fill(plots, read_variables = read_variables, sequence = sequence)

  if args.add2015:
    for plot in plots:
      plot.addPlot(os.path.join("/user/tomc/StopsDilepton/plots/ttG2015", mode, args.selection))

  # Subtract other MC's from data
  if args.subtract:
    for plot in plots:
      for j, h in enumerate(plot.histos[0]):
        if plot.stack[0][j].name != 'TTGJets': plot.histos[1][0].Add(h, -1)
        else:                                  plot.histos[0] = [h]
      plot.stack = Stack([TTG], [data_sample])


  # Get normalization yields from yield histogram
  for plot in plots:
    if plot.name == "yield":
      for i, l in enumerate(plot.histos):
        for j, h in enumerate(l):
          yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+index))
          h.GetXaxis().SetBinLabel(1, "#mu#mu")
          h.GetXaxis().SetBinLabel(2, "e#mu")
          h.GetXaxis().SetBinLabel(3, "ee")
      yields[mode]["MC"] = sum(yields[mode][s.name] for s in plot.stack[0])

  dataMCScale = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')
  logger.info( "Data/MC Scale: %4.4f Yield MC %4.4f Yield Data %4.4f Lumi-scale %4.4f", dataMCScale, yields[mode]["MC"], yields[mode]["data"], lumi_scale )

  for plot in plots: #To get normalized bins in variable binning
    if hasattr(plot, 'binWidth'):
      for histo in sum(plot.histos, []):
        for ib in range(histo.GetXaxis().GetNbins()+1):
	  val = histo.GetBinContent( ib )
	  err = histo.GetBinError( ib )
	  width = histo.GetBinWidth( ib )
	  histo.SetBinContent(ib, val / (width / plot.binWidth))
	  histo.SetBinError(ib, err / (width / plot.binWidth))

    if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
    plotting.draw(plot, 
        plot_directory = os.path.join(plot_directory, args.plot_directory, mode, args.selection),
        ratio = {'yRange':(0.1,1.9)}, 
        logX = False, logY = False, sorting = False, 
        yRange = (0.003, "auto"),
        scaling = {},
        drawObjects = drawObjects( dataMCScale, lumi_scale),
    )
  allPlots[mode] = plots



# Add yields in channels
yields["all"] = {}
for y in yields[allModes[0]]:
  try:    yields["all"][y] = sum(yields[mode][y] for mode in allModes)
  except: yields["all"][y] = 0
dataMCScale = yields["all"]["data"]/(yields["all"]["MC"])


# Write to tex file
columns = [i.name for i in (mc if not args.subtract else [TTG])] + ["MC", "data"]
texdir = "tex"
try:
  os.makedirs("./" + texdir)
except:
  pass
with open("./" + texdir + "/" + args.selection + ".tex", "w") as f:
  f.write("&" + " & ".join(columns) + "\\\\ \n")
  for mode in allModes + ["all"]:
    f.write(mode + " & " + " & ".join([ " %12.1f" % yields[mode][i] for i in columns]) + "\\\\ \n")


# Add the different channels and plot the sums
for plot in allPlots[allModes[0]]:
  logger.info("Adding " + plot.name + " for mode " + allModes[0] + " to all")
  for mode in allModes[1:]:
    for plot2 in (p for p in allPlots[mode] if p.name == plot.name):
      logger.info("Adding " + plot.name + " for mode " + mode + " to all")
      for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
        for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
          if i==k:
            j.Add(l)

for plot in allPlots[allModes[0]]:
  plot.histos[1][0].legendText = "Data 2015+2016 (all)" if args.add2015 else "Data"
  plotting.draw(plot,
        plot_directory = os.path.join(plot_directory, args.plot_directory, "all", args.selection),
        ratio = {'yRange':(0.1,1.9)},
        logX = False, logY = False, sorting = False,
        yRange = (0.003, "auto"),
        scaling = {},
        drawObjects = drawObjects( dataMCScale, lumi_scale ),
  )

logger.info( "Done with prefix %s and selectionString %s", args.selection, selectionStrings[args.selection] )
