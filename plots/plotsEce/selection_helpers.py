import ROOT

def getZCut(mode):
    mZ = 91.2
    zstr = "abs(dl_mass - "+str(mZ)+")"
    if mode.lower()=="onz": return zstr+"<15"
    if mode.lower()=="offz": return zstr+">15"
    return "(1)"

#zMode = "allZ" # 'onZ', 'offZ', 'allZ'

mode_sel = {"doubleMu": "&&".join(["isMuMu==1&&nGoodMuons==2&&nGoodElectrons==0", getZCut('offZ')]) ,\
            "doubleEle": "&&".join(["isEE==1&&nGoodMuons==0&&nGoodElectrons==2", getZCut('offZ')]) ,\
            "muEle": "&&".join(["isEMu==1&&nGoodMuons==1&&nGoodElectrons==1", getZCut('allZ')]) ,\
            "dilepton": "(isEMu==1&&nGoodMuons==1&&nGoodElectrons==1|| ( isMuMu==1&&nGoodMuons==2&&nGoodElectrons==0 || isEE==1&&nGoodMuons==0&&nGoodElectrons==2 ) && abs(dl_mass-91.2)>15)" \
            }

dPhi = [("dPhiJetMET", "Sum$( ( cos(met_phi-JetGood_phi)>cos(0.25) )*(Iteration$<2) )+Sum$( ( cos(met_phi-JetGood_phi)>0.8 )*(Iteration$==0) )==0")]

#c_dl_mt2ll =
#c_dl_mt2bb =
#c_dl_mt2blbl = 

basic_cuts=[ 
    ("mll20", "dl_mass>20"),
    ("l1pt25", "l1_pt>25"),
    ("mIsoVT", "l1_mIsoWP>=5&&l2_mIsoWP>=5"),
    ] + dPhi + [
    ("lepVeto", "nGoodMuons+nGoodElectrons==2"),
    ("looseLeptonVeto", "Sum$(LepGood_pt>15&&LepGood_miniRelIso<0.4)==2"),
]

#lepSel = [("muEle",mode_sel["muEle"])]

lepSel = [("dilep",mode_sel["dilepton"])]
nJet  = [("njet2p" , "nJetGood>=2")]
nBtag = [("nbtag1p" , "nBTag>=1")]
metSig5 = [("metSig5", "(met_pt/sqrt(ht)>5||nJetGood==0)")]
met80 = [("met80", "met_pt>80")]

charge = [("isOS","isOS")]

mc_filters_cut = "Flag_goodVertices&&Flag_HBHENoiseIsoFilter&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_badChargedHadron&&Flag_badMuon"
#all_cuts =  charge + basic_cuts + nJet + nBtag + met80 + metSig5

#all_cuts =  lepSel + charge  +nJet + nBtag + met80 + metSig5 + basic_cuts
all_cuts =  lepSel + charge  +nJet + nBtag + basic_cuts

#for p in all_cuts:
#  print p[1]


selectionString = {"sel": "&&".join( [p[1] for p in all_cuts] ) , "name": "_".join( [p[0] for p in all_cuts] ) }

mc_sel_string = "&&".join([selectionString["sel"],mc_filters_cut]) 
test_sel_string = "&&".join([selectionString["sel"]]) 
#test_sel_string = "&&".join([selectionString["sel"]]) 

#test_sel_string = "isOS&&dl_mass>20&&l1_pt>25&&l1_mIsoWP>=5&&l2_mIsoWP>=5&&Sum$( ( cos(met_phi-JetGood_phi)>cos(0.25) )*(Iteration$<2) )+Sum$( ( cos(met_phi-JetGood_phi)>0.8 )*(Iteration$==0) )==0&&nGoodMuons+nGoodElectrons==2&&Sum$(LepGood_pt>15&&LepGood_miniRelIso<0.4)==2&&nJetGood>=2&&nBTag>=1&&met_pt>80&&(met_pt/sqrt(ht)>5||nJetGood==0)&&dl_mt2ll<100" 
mc_weight_string = "weight*12.9*reweightDilepTriggerBackup*reweightBTag_SF*reweightLeptonSF*reweightLeptonHIPSF*reweightPU12fb"
sig_weight_string = mc_weight_string+"*reweightLeptonFastSimSF"
