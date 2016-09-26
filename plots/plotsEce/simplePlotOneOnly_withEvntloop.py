import ROOT
from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed import *
from math import sqrt, cos, sin, pi, acos
import itertools

from RootTools.core.standard import *

from StopsDilepton.tools.user import plot_directory
plot_path = os.path.join(plot_directory, "trials", "1")
if not os.path.exists( plot_path ): os.makedirs( plot_path )

mc_samples = [DY_HT_LO]
stack = Stack(mc_samples)
sample = DY_HT_LO
sample.reduceFiles(to = 1)   ####small

sample.setSelectionString(["(1)"])
sample.style = styles.fillStyle( sample.color)
#sample.weight = "(1)"

from StopsDilepton.tools.objectSelection import getJets

myjetVars = ['eta','pt','phi','btagCSV', 'id','hadronFlavour']

def getNTrueBJets( data ):
    jets = filter(lambda j: j['pt']>30 and abs(j['eta'])<2.4 and j['id'], getJets(data,jetVars=myjetVars ,jetColl="JetGood"))
    true_bjets = filter(lambda j: abs(j['hadronFlavour'])==5, jets)
    setattr( data, "n_true_bJets", len(true_bjets) )

sequence = [getNTrueBJets]
n_true_bJets  = Plot(
    name = "n_true_bJets",
    texX = 'n true bJets ', texY = 'Number of Events',
    stack = stack,
    variable = ScalarType.uniqueFloat().addFiller(lambda data: data.n_true_bJets),
    binning=[4,0,4],
    #selectionString = "(1)",
    #weight = "(1)",
    )

read_variables = ["weight/F" , "JetGood[pt/F,eta/F,phi/F,btagCSV/F,id/I,hadronFlavour/I]", "nJetGood/I"]
plotting.fill([n_true_bJets], read_variables = read_variables, sequence = sequence)

plotting.draw(n_true_bJets,
    plot_directory = plot_path,
    logX = False, logY = True, #sorting = True, 
    #scaling = {0:1} if not args.noScaling else {},
    yRange = (0.03, "auto"),
    )
            


