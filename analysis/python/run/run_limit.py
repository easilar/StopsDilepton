#!/usr/bin/env python
import os
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument("--metSigMin",      action='store', default=5,                   type=int,                                                                                                         help="metSigMin?")
argParser.add_argument("--metMin",         action='store', default=80,                  type=int,                                                                                                         help="metMin?")
argParser.add_argument("--multiIsoWP",     action='store', default="",                                                                                                                                    help="multiIsoWP?")
argParser.add_argument("--relIso04",       action='store', default=-1,                  type=float,                                                                                                       help="relIso04 cut?")
argParser.add_argument("--estimateDY",     action='store', default='DY',                nargs='?', choices=["DY","DY-DD"],                                                                                help="which DY estimate?")
argParser.add_argument("--estimateTTZ",    action='store', default='TTZ',               nargs='?', choices=["TTZ","TTZ-DD","TTZ-DD-Top16009"],                                                            help="which TTZ estimate?")
argParser.add_argument("--regions",        action='store', default='reducedRegionsNew', nargs='?', choices=["defaultRegions","reducedRegionsA","reducedRegionsB","reducedRegionsAB","reducedRegionsNew"], help="which regions setup?")
argParser.add_argument("--signal",         action='store', default='T2tt',              nargs='?', choices=["T2tt","DM"],                                                                                 help="which signal?")
args = argParser.parse_args()

from StopsDilepton.analysis.SetupHelpers import allChannels
from StopsDilepton.analysis.estimators   import setup, constructEstimatorList, MCBasedEstimate, DataDrivenTTZEstimate, DataDrivenDYEstimate
from StopsDilepton.analysis.regions      import defaultRegions, reducedRegionsA, reducedRegionsB, reducedRegionsAB, reducedRegionsNew, reducedRegionsC
from StopsDilepton.analysis.Cache        import Cache

setup.verbose = False
setup.parameters['metMin']    = args.metMin
setup.parameters['metSigMin'] = args.metSigMin

if args.regions == "defaultRegions":      regions = defaultRegions
elif args.regions == "reducedRegionsA":   regions = reducedRegionsA
elif args.regions == "reducedRegionsB":   regions = reducedRegionsB
elif args.regions == "reducedRegionsAB":  regions = reducedRegionsAB
elif args.regions == "reducedRegionsNew": regions = reducedRegionsNew
elif args.regions == "reducedRegionsC":   regions = reducedRegionsC
else: raise Exception("Unknown regions setup")

estimators = constructEstimatorList(['TTJets','other', args.estimateDY, args.estimateTTZ])

if args.multiIsoWP!="":
    multiIsoWPs = ['VL', 'L', 'M', 'T', 'VT']
    wpMu, wpEle=args.multiIsoWP.split(',')
    from StopsDilepton.tools.objectSelection import multiIsoLepString
    setup.externalCuts.append(multiIsoLepString(wpMu, wpEle, ('l1_index','l2_index')))
    setup.prefixes.append('multiIso'+args.multiIsoWP.replace(',',''))

if args.relIso04>0:
    setup.externalCuts.append("&&".join(["LepGood_relIso04["+ist+"]<"+str(args.relIso04) for ist in ('l1_index','l2_index')]))
    setup.prefixes.append('relIso04sm'+str(int(100*args.relIso04)))

for e in estimators:
    e.initCache(setup.defaultCacheDir())

from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_postProcessed    import *
from StopsDilepton.samples.cmgTuples_FullSimTTbarDM_mAODv2_25ns_postProcessed import *
from StopsDilepton.analysis.u_float                                           import u_float
from math                                                                     import sqrt

##https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYSignalSystematicsRun2
from StopsDilepton.tools.user           import combineReleaseLocation
from StopsDilepton.tools.cardFileWriter import cardFileWriter

limitPrefix = args.regions
limitDir    = os.path.join(setup.analysis_results, setup.prefix(), args.estimateDY, args.estimateTTZ, 'cardFiles', args.signal, limitPrefix)
overWrite   = False
useCache    = True
verbose     = True

if not os.path.exists(limitDir): os.makedirs(limitDir)
cacheFileName = os.path.join(limitDir, 'calculatedLimits.pkl')
limitCache    = Cache(cacheFileName, verbosity=2)

if   args.signal == "T2tt": fastSim = True
elif args.signal == "DM":   fastSim = False

def wrapper(s):
    c = cardFileWriter.cardFileWriter()
    c.releaseLocation = combineReleaseLocation

    cardFileName = os.path.join(limitDir, s.name+'.txt')
    if not os.path.exists(cardFileName) or overWrite:
	counter=0
	c.reset()
	c.addUncertainty('PU',       'lnN')
	c.addUncertainty('topPt',    'lnN')
	c.addUncertainty('JEC',      'lnN')
	c.addUncertainty('JER',      'lnN')
	c.addUncertainty('SFb',      'lnN')
	c.addUncertainty('SFl',      'lnN')
        if fastSim:
 	  c.addUncertainty('SFFS',     'lnN')
  	  c.addUncertainty('leptonSF', 'lnN')

	eSignal = MCBasedEstimate(name=s.name, sample={channel:s for channel in allChannels}, cacheDir=setup.defaultCacheDir() )
        for r in regions[1:]:
            for channel in ['MuMu', 'EE', 'EMu']:                                         # for channel in ['all']:
                niceName = ' '.join([channel, r.__str__()])
                binname = 'Bin'+str(counter)
                counter += 1
                total_exp_bkg = 0
                c.addBin(binname, [e.name for e in estimators], niceName)
                for e in estimators:
                    expected = e.cachedEstimate(r, channel, setup)
                    total_exp_bkg += expected.val
                    c.specifyExpectation(binname, e.name, expected.val )

                    if expected.val>0:
                        c.specifyUncertainty('PU',    binname, e.name, 1 + e.PUSystematic(         r, channel, setup).val )
                        c.specifyUncertainty('JEC',   binname, e.name, 1 + e.JECSystematic(        r, channel, setup).val )
                        c.specifyUncertainty('JER',   binname, e.name, 1 + e.JERSystematic(        r, channel, setup).val )
                        c.specifyUncertainty('topPt', binname, e.name, 1 + e.topPtSystematic(      r, channel, setup).val )
                        c.specifyUncertainty('SFb',   binname, e.name, 1 + e.btaggingSFbSystematic(r, channel, setup).val )
                        c.specifyUncertainty('SFl',   binname, e.name, 1 + e.btaggingSFlSystematic(r, channel, setup).val )

                        #MC bkg stat (some condition to neglect the smaller ones?)
                        uname = 'Stat_'+binname+'_'+e.name
                        c.addUncertainty(uname, 'lnN')
                        c.specifyUncertainty('Stat_'+binname+'_'+e.name, binname, e.name, 1+expected.sigma/expected.val )

                c.specifyObservation(binname, int(total_exp_bkg) )

                #signal
                e = eSignal
                if fastSim: signalSetup = setup.sysClone(sys={'reweight':['reweightLeptonFastSimSF']}, parameters={'useTriggers':False})
                else:       signalSetup = setup.sysClone(parameters={'useTriggers':False})
                signal = e.cachedEstimate(r, channel, signalSetup)

                c.specifyExpectation(binname, 'signal', signal.val )

                if signal.val>0:
                    c.specifyUncertainty('PU',  binname, 'signal', 1 + e.PUSystematic(         r, channel, signalSetup).val )
                    c.specifyUncertainty('JEC', binname, 'signal', 1 + e.JECSystematic(        r, channel, signalSetup).val )
                    c.specifyUncertainty('JER', binname, 'signal', 1 + e.JERSystematic(        r, channel, signalSetup).val )
                    c.specifyUncertainty('SFb', binname, 'signal', 1 + e.btaggingSFbSystematic(r, channel, signalSetup).val )
                    c.specifyUncertainty('SFl', binname, 'signal', 1 + e.btaggingSFlSystematic(r, channel, signalSetup).val )
                    if fastSim: 
                      c.specifyUncertainty('leptonSF', binname, 'signal', 1 + e.leptonFSSystematic(    r, channel, signalSetup).val )
                      c.specifyUncertainty('SFFS',     binname, 'signal', 1 + e.btaggingSFFSSystematic(r, channel, signalSetup).val )

                    #signal MC stat added in quadrature with PDF uncertainty: 10% uncorrelated
                    uname = 'Stat_'+binname+'_signal'
                    c.addUncertainty(uname, 'lnN')
                    c.specifyUncertainty(uname, binname, 'signal', 1 + sqrt(0.1**2 + signal.sigma/signal.val) )

                if signal.val<=0.01 and total_exp_bkg<=0.01 or total_exp_bkg<=0:# or (total_exp_bkg>300 and signal.val<0.05):
                    if verbose: print "Muting bin %s. Total sig: %f, total bkg: %f"%(binname, signal.val, total_exp_bkg)
                    c.muted[binname] = True
                else:
                    if verbose: print "NOT Muting bin %s. Total sig: %f, total bkg: %f"%(binname, signal.val, total_exp_bkg)

        c.addUncertainty('Lumi', 'lnN')
        c.specifyFlatUncertainty('Lumi', 1.046)
        cardFileName = c.writeToFile(cardFileName)
    else:
        print "File %s found. Reusing."%cardFileName

    if   args.signal == "DM":   sConfig = s.mChi, s.mPhi, s.type
    elif args.signal == "T2tt": sConfig = s.mStop, s.mNeu

    if useCache and not overWrite and limitCache.contains(s):
      res = limitCache.get(sConfig)
    else:
      res = c.calcLimit(cardFileName)
      limitCache.add(sConfig, res, save=True)

    try:
      if res: 
	if   args.signal == "DM":   sString = "mChi %i mPhi %i type %i" % sConfig
	elif args.signal == "T2tt": sString = "mStop %i mNeu %i" % sConfig
        print "Result: %i obs %5.3f exp %5.3f -1sigma %5.3f +1sigma %5.3f"%(sString, res['-1.000'], res['0.500'], res['0.160'], res['0.840'])
    except:
      print "Something wrong with the limit: %r"%res
    return sConfig, res

if   args.signal == "T2tt": jobs = signals_T2tt 
elif args.signal == "DM":   jobs = signals_TTDM

results = map(wrapper, jobs)

# Make histograms for T2tt
if args.signal == "T2tt":
  exp      = ROOT.TH2F("exp", "exp", 1000/25, 0, 1000, 1000/25, 0, 1000)
  exp_down = exp.Clone("exp_down")
  exp_up   = exp.Clone("exp_up")
  obs      = exp.Clone("obs")

  for r in results:
    s, res = r
    mStop, mNeu = r
    if type != "scalar": continue
    for hist, qE in [(exp, '0.500'), (exp_up, '0.160'), (exp_down, '0.840'), (obs, '-1.000')]:
      try:
	  hist.Fill(mStop, mNeu, res[qE])
      except:
	  print "Something failed for mChi %i mPhi %i res %s"%(mStop, mNeu, res)

  limitResultsFilename = os.path.join(os.path.join(setup.analysis_results, setup.prefix(), args.estimateDY, args.estimateTTZ, 'limits', args.signal, limitPrefix,'limitResults.root'))
  if not os.path.exists(os.path.dirname(limitResultsFilename)):
      os.makedirs(os.path.dirname(limitResultsFilename))

  outfile = ROOT.TFile(limitResultsFilename, "recreate")
  exp      .Write()
  exp_down .Write()
  exp_up   .Write()
  obs      .Write()
  outfile.Close()
  print "Written %s"%limitResultsFilename


# Make table for DM
if args.signal == "DM":
  # Create table
  texdir = os.path.join(os.path.join(setup.analysis_results, setup.prefix(), args.estimateDY, args.estimateTTZ, 'limits', limitPrefix))

  for type in sorted(set([type_ for ((mChi, mPhi, type_), res) in results])):
    chiList = sorted(set([mChi  for ((mChi, mPhi, type_), res) in results if type_ == type]))
    phiList = sorted(set([mPhi  for ((mChi, mPhi, type_), res) in results if type_ == type]))
    print "Writing to " + texdir + "/" + type + ".tex"
    with open(texdir + "/" + type + ".tex", "w") as f:
      f.write("\\begin{tabular}{cc|" + "c"*len(phiList) + "} \n")
      f.write(" & & \multicolumn{" + str(len(phiList)) + "}{c}{$m_\\phi$ (GeV)} \\\\ \n")
      f.write("& &" + " & ".join(str(x) for x in phiList) + "\\\\ \n \\hline \\hline \n")
      for chi in chiList:
	resultList = []
	for phi in phiList:
	  result = ''
	  try:
	    for ((c, p, t), r) in results:
	      if c == chi and p == phi and t == type:
		  result = "%.3f" % r['0.500']
	  except:
	    pass
	  resultList.append(result)
	if chi == chiList[0]: f.write("\\multirow{" + str(len(chiList)) + "}{*}{$m_\\chi$ (GeV)}")
	f.write(" & " + str(chi) + " & " + " & ".join(resultList) + "\\\\ \n")
      f.write(" \\end{tabular}")
