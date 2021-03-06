import copy, os, sys
from RootTools.core.Sample import Sample
import ROOT

from StopsDilepton.tools.user import data_directory
from StopsDilepton.samples.color import color

# Take post processing directory if defined in main module
try:
  import sys
  postProcessing_directory = sys.modules['__main__'].postProcessing_directory
except:
  postProcessing_directory = "postProcessed_80X_v12/dilepTiny/"

DY_M5to50_HT = ["DYJetsToLL_M5to50_LO_lheHT100", "DYJetsToLL_M5to50_HT100to200_comb", "DYJetsToLL_M5to50_HT200to400_comb", "DYJetsToLL_M5to50_HT400to600", "DYJetsToLL_M5to50_HT600toInf_comb"] 
DY_M50_HT = ["DYJetsToLL_M50_LO_lheHT100", "DYJetsToLL_M50_HT100to200_comb", "DYJetsToLL_M50_HT200to400_comb", "DYJetsToLL_M50_HT400to600_ext", "DYJetsToLL_M50_HT600toInf_comb"] 

dirs = {}
dirs['DY']               = ["DYJetsToLL_M50", "DYJetsToLL_M10to50" ]
dirs['DY_LO']            = ["DYJetsToLL_M10to50_LO", "DYJetsToLL_M50_LO"]
#dirs['DY_HT_LO']         = ["DYJetsToLL_M50_LO_lheHT100", "DYJetsToLL_M50_HT100to200_ext", "DYJetsToLL_M50_HT200to400_ext", "DYJetsToLL_M50_HT400to600_ext", "DYJetsToLL_M50_HT600toInf_comb", "DYJetsToLL_M10to50_LO"]
dirs['DY_HT_LO']         =  DY_M50_HT + DY_M5to50_HT
dirs['TTJets']           = ["TTJets"]
#dirs['TTJets_LO']        = ["TTJets_LO"]
dirs['TTLep_pow']        = ["TT_pow_ext3_comb"]

dirs['TTJets_Lep']       = ["TTJets_DiLepton_comb", "TTJets_SingleLeptonFromTbar_comb", "TTJets_SingleLeptonFromT"]
dirs['TTJets_Dilep']       = ["TTJets_DiLepton_comb"]
dirs['TTJets_Singlelep']       = ["TTJets_SingleLeptonFromTbar_comb", "TTJets_SingleLeptonFromT"]
#dirs['TTJets_HT_LO']     = ["TTJets_LO_HT600to800_comb", "TTJets_LO_HT800to1200_comb", "TTJets_LO_HT1200to2500_comb", "TTJets_LO_HT2500toInf"]
dirs['singleTop']        = ["TBar_tWch", "T_tWch"]
dirs['Top']              = dirs['singleTop'] + dirs['TTJets_Lep']
dirs['Top_pow']          = dirs['TTLep_pow'] + dirs['singleTop'] 
dirs['TZQ']              = ["tZq_ll", "tZq_nunu"]
dirs['TZQ']              = ["tZq_ll"]
dirs['TTW']              = ["TTWToLNu", "TTWToQQ"]
dirs['TTH']              = [ \
#        "TTHbb_ext3", 
        "TTHnobb_mWCutfix_ch0"]
dirs['TTZtoLLNuNu']      = ["TTZToLLNuNu"]
dirs['TTZtoQQ']          = ["TTZToQQ"]
dirs['TTZ']              = ["TTZToLLNuNu", "TTZToQQ"]
dirs['TTZ_LO']          = ["TTZ_LO"]
dirs['TTXNoZ']           = dirs['TTH'] + dirs['TTW'] + dirs['TZQ']
dirs['TTX']              = dirs['TTXNoZ'] + dirs['TTZ_LO']
dirs['WJetsToLNu']       = ["WJetsToLNu"]
#dirs['WJetsToLNu_LO']    = ["WJetsToLNu_LO"]
dirs['WJetsToLNu_HT']    = ["WJetsToLNu_HT100to200_comb", "WJetsToLNu_HT200to400_comb", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600to800", "WJetsToLNu_HT800to1200", "WJetsToLNu_HT1200to2500", "WJetsToLNu_HT2500toInf"]
dirs['diBosonInclusive'] = ["WW", "WZ", "ZZ"]
dirs['WW']               = ["WWTo1L1Nu2Q", "WWToLNuQQ_comb"]
dirs['WW_']              = ["WWTo1L1Nu2Q", "WWToLNuQQ_comb","WWTo2L2Nu"]
dirs['VVTo2L2Nu']        = ["VVTo2L2Nu"]
dirs['WZ']               = ["WZTo1L1Nu2Q", "WZTo1L3Nu", "WZTo2L2Q", "WZTo3LNu"]
dirs['ZZ']              = ["ZZTo2L2Q", "ZZTo2Q2Nu"]
dirs['ZZ_']              = ["ZZTo2L2Q", "ZZTo2Q2Nu","ZZTo2L2Nu"]
dirs['diBoson']          = dirs['WW'] + dirs['WZ'] + dirs['ZZ'] + dirs['VVTo2L2Nu']
dirs['triBoson']         = ["WWZ","WZZ","ZZZ"] 
dirs['multiBoson']       = dirs['diBoson'] + dirs['triBoson']
#dirs['QCD_HT']           = ["QCD_HT100to200", "QCD_HT200to300", "QCD_HT300to500", "QCD_HT500to700", "QCD_HT700to1000", "QCD_HT1000to1500", "QCD_HT1500to2000", "QCD_HT2000toInf"]
#dirs['QCD_Mu5']          = ["QCD_Pt20to30_Mu5", "QCD_Pt50to80_Mu5", "QCD_Pt80to120_Mu5", "QCD_Pt120to170_Mu5", "QCD_Pt170to300_Mu5", "QCD_Pt300to470_Mu5", "QCD_Pt470to600_Mu5", "QCD_Pt600to800_Mu5", "QCD_Pt800to1000_Mu5", "QCD_Pt1000toInf_Mu5"]
#dirs['QCD_EM+bcToE']     = ["QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE", "QCD_Pt15to20_EMEnriched", "QCD_Pt20to30_EMEnriched", "QCD_Pt50to80_EMEnriched", "QCD_Pt80to120_EMEnriched", "QCD_Pt120to170_EMEnriched", "QCD_Pt170to300_EMEnriched"]
#dirs['QCD_EM+bcToE']    = ["QCD_Pt_15to20_bcToE", "QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE", "QCD_Pt15to20_EMEnriched", "QCD_Pt20to30_EMEnriched", "QCD_Pt30to50_EMEnriched", "QCD_Pt50to80_EMEnriched", "QCD_Pt80to120_EMEnriched", "QCD_Pt120to170_EMEnriched", "QCD_Pt170to300_EMEnriched", "QCD_Pt300toInf_EMEnriched"]
#dirs['QCD_Mu5+EM+bcToE'] = ["QCD_Pt20to30_Mu5", "QCD_Pt50to80_Mu5", "QCD_Pt80to120_Mu5", "QCD_Pt120to170_Mu5", "QCD_Pt170to300_Mu5", "QCD_Pt300to470_Mu5", "QCD_Pt470to600_Mu5", "QCD_Pt600to800_Mu5", "QCD_Pt800to1000_Mu5", "QCD_Pt1000toInf_Mu5", "QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE", "QCD_Pt15to20_EMEnriched", "QCD_Pt20to30_EMEnriched", "QCD_Pt50to80_EMEnriched", "QCD_Pt80to120_EMEnriched", "QCD_Pt120to170_EMEnriched", "QCD_Pt170to300_EMEnriched"]
#dirs['QCD_Mu5+EM+bcToE']= ["QCD_Pt20to30_Mu5", "QCD_Pt50to80_Mu5", "QCD_Pt80to120_Mu5", "QCD_Pt120to170_Mu5", "QCD_Pt170to300_Mu5", "QCD_Pt300to470_Mu5", "QCD_Pt470to600_Mu5", "QCD_Pt600to800_Mu5", "QCD_Pt800to1000_Mu5", "QCD_Pt1000toInf_Mu5", "QCD_Pt_15to20_bcToE", "QCD_Pt_20to30_bcToE", "QCD_Pt_30to80_bcToE", "QCD_Pt_80to170_bcToE", "QCD_Pt_170to250_bcToE", "QCD_Pt_250toInf_bcToE", "QCD_Pt15to20_EMEnriched", "QCD_Pt20to30_EMEnriched", "QCD_Pt30to50_EMEnriched", "QCD_Pt50to80_EMEnriched", "QCD_Pt80to120_EMEnriched", "QCD_Pt120to170_EMEnriched", "QCD_Pt170to300_EMEnriched", "QCD_Pt300toInf_EMEnriched"]
#dirs['QCD']              = ["QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120", "QCD_Pt120to170", "QCD_Pt170to300", "QCD_Pt300to470", "QCD_Pt470to600", "QCD_Pt600to800", "QCD_Pt800to1000", "QCD_Pt1000to1400", "QCD_Pt1400to1800", "QCD_Pt1800to2400", "QCD_Pt2400to3200"]
#dirs['QCD']             = ["QCD_Pt10to15", "QCD_Pt15to30", "QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120", "QCD_Pt120to170", "QCD_Pt170to300", "QCD_Pt300to470", "QCD_Pt470to600", "QCD_Pt600to800", "QCD_Pt800to1000", "QCD_Pt1000to1400", "QCD_Pt1400to1800", "QCD_Pt1800to2400", "QCD_Pt2400to3200", "QCD_Pt3200"]

#dirs['WGToLNuG']     = ["WGToLNuG"]
#dirs['ZGTo2LG']      = ["ZGTo2LG"]
#dirs['WGJets']       = ["WGJets"]
#dirs['ZGJets']       = ["ZGJets"]

directories = { key : [ os.path.join( data_directory, postProcessing_directory, dir) for dir in dirs[key]] for key in dirs.keys()}

DY             = Sample.fromDirectory(name="DY",               treeName="Events", isData=False, color=color.DY,              texName="DY",                                directory=directories['DY'])
DY_LO          = Sample.fromDirectory(name="DY_LO",            treeName="Events", isData=False, color=color.DY,              texName="DY (LO)",                           directory=directories['DY_LO'])
DY_HT_LO       = Sample.fromDirectory(name="DY_HT_LO",         treeName="Events", isData=False, color=color.DY,              texName="DY (LO,HT)",                        directory=directories['DY_HT_LO'])
TTJets         = Sample.fromDirectory(name="TTJets",           treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}",                          directory=directories['TTJets'])
TTJets_Lep     = Sample.fromDirectory(name="TTJets_Lep",       treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}(lep)",                     directory=directories['TTJets_Lep'])
TTJets_Singlelep= Sample.fromDirectory(name="TTJets_Singlelep",           treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}",                          directory=directories['TTJets_Singlelep'])
TTJets_Dilep    = Sample.fromDirectory(name="TTJets_Dilep",           treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}",                          directory=directories['TTJets_Dilep'])
#TTJets_LO      = Sample.fromDirectory(name="TTJets_LO",        treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t} + Jets (LO)",              directory=directories['TTJets_LO'])
TTLep_pow      = Sample.fromDirectory(name="TTLep_pow",        treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t} + Jets (lep,pow)",         directory=directories['TTLep_pow'])
Top            = Sample.fromDirectory(name="Top",              treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}/single-t",                 directory=directories['Top'])
Top_pow            = Sample.fromDirectory(name="Top_pow",              treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t}/single-t(powHeg)",                 directory=directories['Top_pow'])
#TTJets_HT_LO   = Sample.fromDirectory(name="TTJets_HT_LO",     treeName="Events", isData=False, color=color.TTJets,          texName="t#bar{t} + Jets (HT,LO)",           directory=directories['TTJets_HT_LO'])
singleTop      = Sample.fromDirectory(name="singleTop",        treeName="Events", isData=False, color=color.singleTop,       texName="single top",                        directory=directories['singleTop'])
TTX            = Sample.fromDirectory(name="TTX",              treeName="Events", isData=False, color=color.TTX,             texName="t#bar{t}H/W/Z, tZq",                directory=directories['TTX'])
TTXNoZ         = Sample.fromDirectory(name="TTXNoZ",           treeName="Events", isData=False, color=color.TTXNoZ,          texName="t#bar{t}H/W, tZq",                  directory=directories['TTXNoZ'])
TTH            = Sample.fromDirectory(name="TTH",              treeName="Events", isData=False, color=color.TTH,             texName="t#bar{t}H",                         directory=directories['TTH'])
TTW            = Sample.fromDirectory(name="TTW",              treeName="Events", isData=False, color=color.TTW,             texName="t#bar{t}W",                         directory=directories['TTW'])
TTZ            = Sample.fromDirectory(name="TTZ",              treeName="Events", isData=False, color=color.TTZ,             texName="t#bar{t}Z",                         directory=directories['TTZ'])
TTZ_LO        = Sample.fromDirectory(name="TTZ_LO",              treeName="Events", isData=False, color=color.TTZ,             texName="t#bar{t}Z",                         directory=directories['TTZ_LO'])
TTZtoLLNuNu    = Sample.fromDirectory(name="TTZtoNuNu",        treeName="Events", isData=False, color=color.TTZtoLLNuNu,     texName="t#bar{t}Z (l#bar{l}/#nu#bar{#nu})", directory=directories['TTZtoLLNuNu'])
TTZtoQQ        = Sample.fromDirectory(name="TTZtoQQ",          treeName="Events", isData=False, color=color.TTZtoQQ,         texName="t#bar{t}Z (q#bar{q})",              directory=directories['TTZtoQQ'])
TZQ            = Sample.fromDirectory(name="TZQ",              treeName="Events", isData=False, color=color.TZQ,             texName="tZq",                               directory=directories['TZQ'])
WJetsToLNu     = Sample.fromDirectory(name="WJetsToLNu",       treeName="Events", isData=False, color=color.WJetsToLNu,      texName="W(l,#nu) + Jets",                   directory=directories['WJetsToLNu'])
#WJetsToLNu_LO  = Sample.fromDirectory(name="WJetsToLNu_LO",    treeName="Events", isData=False, color=color.WJetsToLNu,      texName="W(l,#nu) + Jets (LO)",              directory=directories['WJetsToLNu_LO'])
#WJetsToLNu_HT  = Sample.fromDirectory(name="WJetsToLNu_HT",    treeName="Events", isData=False, color=color.WJetsToLNu,      texName="W(l,#nu) + Jets (HT)",              directory=directories['WJetsToLNu_HT'])
diBoson        = Sample.fromDirectory(name="diBoson",          treeName="Events", isData=False, color=color.diBoson,         texName="VV (excl.)",                        directory=directories['diBoson'])
diBosonInclusive = Sample.fromDirectory(name="diBosonInclusive",treeName="Events", isData=False, color=color.diBoson,        texName="VV (incl.)",                        directory=directories['diBosonInclusive'])
ZZ             = Sample.fromDirectory(name="ZZ",               treeName="Events", isData=False, color=color.ZZ,              texName="ZZ",                                directory=directories['ZZ_'])
ZZNo2L2Nu      = Sample.fromDirectory(name="ZZNo2L2Nu",        treeName="Events", isData=False, color=color.ZZ,              texName="ZZ (no 2L2Nu)",                     directory=directories['ZZ'])
WZ             = Sample.fromDirectory(name="WZ",               treeName="Events", isData=False, color=color.WZ,              texName="WZ",                                directory=directories['WZ'])
WW             = Sample.fromDirectory(name="WW",               treeName="Events", isData=False, color=color.WW,              texName="WW",                                directory=directories['WW_'])
WWNo2L2Nu      = Sample.fromDirectory(name="WWNo2L2Nu",        treeName="Events", isData=False, color=color.WW,              texName="WW (no 2L2Nu)",                     directory=directories['WW'])
VVTo2L2Nu      = Sample.fromDirectory(name="VVTo2L2Nu",               treeName="Events", isData=False, color=color.VV,              texName="VV to ll#nu#nu",             directory=directories['VVTo2L2Nu'])
triBoson       = Sample.fromDirectory(name="triBoson",         treeName="Events", isData=False, color=color.triBoson,        texName="WWZ,WZZ,ZZZ",                       directory=directories['triBoson'])
multiBoson     = Sample.fromDirectory(name="multiBoson",       treeName="Events", isData=False, color=color.diBoson,         texName="multi boson",                       directory=directories['multiBoson'])
#QCD_HT         = Sample.fromDirectory(name="QCD_HT",           treeName="Events", isData=False, color=color.QCD,             texName="QCD (HT)",                          directory=directories['QCD_HT'])
#QCD_Mu5        = Sample.fromDirectory(name="QCD_Mu5",          treeName="Events", isData=False, color=color.QCD,             texName="QCD (Mu5)",                         directory=directories['QCD_Mu5'])
#QCD_EMbcToE    = Sample.fromDirectory(name="QCD_EM+bcToE",     treeName="Events", isData=False, color=color.QCD,             texName="QCD (Em+bcToE)",                    directory=directories['QCD_EM+bcToE'])
#QCD_Mu5EMbcToE = Sample.fromDirectory(name="QCD_Mu5+EM+bcToE", treeName="Events", isData=False, color=color.QCD,             texName="QCD (Mu5+Em+bcToE)",                directory=directories['QCD_Mu5+EM+bcToE'])
#QCD_Pt         = Sample.fromDirectory(name="QCD",              treeName="Events", isData=False, color=color.QCD,             texName="QCD",                               directory=directories['QCD'])

#WGToLNuG = Sample.fromDirectory(name="WGToLNuG",       treeName="Events", isData=False, color=color.diBoson,       texName="WGToLNuG",                       directory=directories['WGToLNuG'])
#ZGTo2LG  = Sample.fromDirectory(name="ZGTo2LG",       treeName="Events", isData=False, color=color.diBoson,        texName="ZGTo2LG",                       directory=directories['ZGTo2LG'] )
#WGJets   = Sample.fromDirectory(name="WGJets",       treeName="Events", isData=False, color=color.diBoson,         texName="WGJets",                       directory=directories['WGJets']  )
#ZGJets   = Sample.fromDirectory(name="ZGJets",       treeName="Events", isData=False, color=color.diBoson,         texName="ZGJets",                       directory=directories['ZGJets']  )
