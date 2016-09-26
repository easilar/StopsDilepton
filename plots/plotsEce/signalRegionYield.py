import ROOT
from math import sqrt, cos, sin, pi, acos
import itertools

from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed import *
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_postProcessed import *
from selection_helpers import *

#mc_samples = [ Top ] + [diBoson] + [DY_HT_LO, TTZ_LO, TTW, triBoson]
mc_samples = [DY_HT_LO]

bm_signals = [("700/50",T2tt_700_50),("650/300",T2tt_650_300),("450/250",T2tt_450_250)] 

#mc_weight_string  = "weight*reweightDilepTriggerBackup*reweightBTag_SF*reweightLeptonSF*reweightLeptonHIPSF"
#sig_weight_string = "weight*reweightDilepTriggerBackup*reweightBTag_SF*reweightLeptonSF*reweightLeptonHIPSF*reweightLeptonFastSimSF"
#sig_weight_string = "weight"
#mc_weight_string  = "weight"

mc_weight_string  = mc_weight_string+"*12.88"
#sig_weight_string = sig_weight_string+"*12.88"

#mcFilterCut   = "Flag_goodVertices&&Flag_HBHENoiseIsoFilter&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_badChargedHadron&&Flag_badMuon"

mc_selectionString = test_sel_string
#sig_selectionString = selectionString["sel"]

#yield_sig_450_1= {"T2tt_450_1": T2tt_450_1.getYieldFromDraw( selectionString = sig_selectionString , weightString = sig_weight_string)['val']}

#print sig_selectionString

#print "signal yield :" , yield_sig_450_1
print "MC sel string:" , mc_selectionString


#yield_mc     = {s.name: s.getYieldFromDraw( selectionString = mc_selectionString , weightString = mc_weight_string)['val'] for s in mc_samples}
#for s in mc_samples :
#  print s.name , yield_mc[s.name]

#sum_mc = sum(yield_mc[s.name] for s in mc_samples)



##yield_sig    = {s[1].name: s[1].getYieldFromDraw( selectionString = sig_selectionString , weightString = sig_weight_string)['val'] for s in bm_signals}




