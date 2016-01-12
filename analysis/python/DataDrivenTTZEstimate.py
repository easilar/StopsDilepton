from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
from u_float import u_float
from StopsDilepton.tools.helpers import printHeader

class DataDrivenTTZEstimate(SystematicBaseClass):
  def __init__(self, name, nJets, nBTags, cacheDir=None):
    super(DataDrivenTTZEstimate, self).__init__(name, cacheDir=cacheDir)
    self.nJets = nJets
    self.nBTags = nBTags
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    printHeader("DD TTZ prediction for '%s' channel %s" %(self.name, channel))

    #Sum of all channels for 'all'
    if channel=='all':
      return sum( [ self.cachedEstimate(region, c, channel, setup) for c in ['MuMu', 'EE', 'EMu'] ] )
    else:
      #Data driven for EE, EMu and  MuMu. 
      preSelection = setup.preselection('MC', channel=channel)

      #check lumi consistency
      assert abs(1.-setup.lumi[channel]/setup.sample['Data'][channel]['lumi'])<0.01, "Lumi specified in setup %f does not match lumi in data sample %f in channel %s"%(setup.lumi[channel], setup.sample['Data'][channel]['lumi'], channel)
      selection_MC_2l = "&&".join([region.cutString(setup.sys['selectionModifier']), preSelection['cut']])
      weight = preSelection['weightStr']
      yield_MC_2l =  setup.lumi[channel]/1000.*u_float(getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = selection_MC_2l, weight=weight, returnError = True) )
      if setup.verbose: print "yield_MC_2l: %s"%yield_MC_2l 
      
      electronSelection_loosePt = "Sum$(LepGood_pt>=10&&abs(LepGood_eta)<2.4&&abs(LepGood_pdgId)==11&&LepGood_miniRelIso<0.2&&LepGood_convVeto&&LepGood_lostHits==0&&LepGood_sip3d<4.0&&abs(LepGood_dxy)<0.05&&abs(LepGood_dz)<0.1&&((abs(LepGood_eta)>=0.&&abs(LepGood_eta)<0.8&&LepGood_mvaIdSpring15>0.87)||(abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479&&LepGood_mvaIdSpring15>0.60)||(abs(LepGood_eta)>=1.57&&abs(LepGood_eta)<999.&&LepGood_mvaIdSpring15>0.17)))"
      muonSelection_loosePt = "Sum$(LepGood_pt>=10&&abs(LepGood_eta)<2.4&&abs(LepGood_pdgId)==13&&LepGood_miniRelIso<0.2&&LepGood_sip3d<4.0&&abs(LepGood_dxy)<0.05&&abs(LepGood_dz)<0.1&&LepGood_mediumMuonId==1)"
      
      #mu_mu_mu
      MuMuMuSelection = "nGoodMuons>=2" + '&&' + muonSelection_loosePt + "==3"
      if setup.useTriggers: MuMuMuSelection += '&&HLT_3mu'
      #e_e_e
      EEESelection = "nGoodElectrons>=2" + '&&' + electronSelection_loosePt + "==3"
     if setup.useTriggers: EEESelection += '&&HLT_3e'
      #e_e_mu
      EEMuSelection = "(nGoodMuons+nGoodElectrons)>=2" + "&&" + electronSelection_loosePt + "==2&&" + muonSelection_loosePt + "==1" 
      if setup.useTriggers: EEMuSelection += '&&HLT_2e1mu'
      #mu_mu_e
      MuMuESelection = "(nGoodMuons+nGoodElectrons)>=2" + "&&" + electronSelection_loosePt + "==1&&" + muonSelection_loosePt + "==2" 
      if setup.useTriggers: MuMuESelection += '&&HLT_2mu1e'
      
      MC_hadronSelection = setup.selection('MC', metMin = 0., metSigMin=0., dPhiJetMet=0.25, nJets = self.nJets, nBTags= self.nBTags, hadronicSelection = True)['cut']
      data_hadronSelection = setup.selection('Data', metMin = 0., metSigMin=0., dPhiJetMet=0.25, nJets = self.nJets, nBTags= self.nBTags, hadronicSelection = True)['cut']

      MC_MuMuMu = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        MC_hadronSelection,
        MuMuMuSelection
      ])
      MC_EEE = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        MC_hadronSelection,
        EEESelection
      ])
      MC_EEMu = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        MC_hadronSelection,
        EEMuSelection
      ])
      MC_MuMuE = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        MC_hadronSelection,
        MuMuESelection
      ])

      MC_3l = "("+MuMuMuSelection+")||("+EEESelection+")||("+EEMuSelection+")||("+MuMuESelection+")"
      
      data_MuMuMu = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        data_hadronSelection,
        MuMuMuSelection
      ])
      data_EEE = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        data_hadronSelection,
        EEESelection
      ])
      data_EEMu = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        data_hadronSelection,
        EEMuSelection
      ])
      data_MuMuE = "&&".join([ ####STILL NEED SOMETHING TO LOOK AT Z-PEAK-> GET Z_PT FROM 3 LEPTONS
        data_hadronSelection,
        MuMuESelection
      ])


      ######IS THIS THE RIGHT LUMI????
      yield_MC_3l = setup.lumi[channel]/1000.*u_float( getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = MC_3l, weight=weight, returnError = True))
      if setup.verbose: print "yield_MC_looseSelection_3l: %s"%yield_MC_3l 
      yield_data_MuMuMu = u_float( getYieldFromChain(setup.sample['Data']['MuMu']['chain'], cutString = data_MuMuMu, weight=weight, returnError = True))
      if setup.verbose: print "yield_data_looseSelection_MuMuMu: %s"%yield_data_MuMuMu
      yield_data_EEE = u_float( getYieldFromChain(setup.sample['Data']['EE']['chain'], cutString = data_EEE, weight=weight, returnError = True))
      if setup.verbose: print "yield_data_looseSelection_EEE: %s"%yield_data_EEE
      yield_data_EMu = u_float( getYieldFromChain(setup.sample['Data']['EMu']['chain'], cutString = "("+data_MuMuE+'||'+data_EEMu+')', weight=weight, returnError = True))
      if setup.verbose: print "yield_data_looseSelection_EMu: %s"%yield_data_EMu
      
      yield_data_3l = yield_data_MuMuMu+yield_data_EEE+yield_data_EMu
      if setup.verbose: print "yield_data_3l: %s"%yield_data_3l
      
      #electroweak subtraction
      print "\n Substracting electroweak backgrounds from data: \n"
      yield_other = u_float(0., 0.) 
      for s in ['TTJets' , 'DY', 'other']:
        yield_other+= setup.lumi[channel]/1000.* u_float(getYieldFromChain(setup.sample[s][channel]['chain'], cutString = MC_3l,  weight=weight, returnError=True))
        if setup.verbose: print "yield_looseSelection_other %s added, now: %s"%(s, yield_other)
        
      normRegYield = yield_data_3l - yield_other
      if normRegYield.val<0: print "\n !!!Warning!!! \n Negative normalization region yield data: (%s), MC: (%s) \n"%(yield_data_3l, yield_other)

      print  "normRegYield", normRegYield
      return u_float(0., 0.) 
      
