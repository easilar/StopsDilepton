import ROOT
from StopsDilepton.samples.cmgTuples_Spring16_mAODv2_postProcessed import *
from math import sqrt, cos, sin, pi, acos
import itertools

from RootTools.core.standard import *

from StopsDilepton.tools.user import plot_directory
plot_path = os.path.join(plot_directory, "trials", "1")
if not os.path.exists( plot_path ): os.makedirs( plot_path )

sample = DY_HT_LO
sample.reduceFiles(to = 1)   ####small
chain = sample.chain
sample.style = styles.fillStyle( sample.color)

histo_0b = ROOT.TH1F("histo_0b" , "nbtag" , 8,0,8)
chain.Draw("nBTag>>histo_0b","Sum$(abs(JetGood_hadronFlavour)==5)==0")
histo_1pb = ROOT.TH1F("histo_1pb" , "nbtag" , 8,0,8)
chain.Draw("nBTag>>histo_1pb","Sum$(abs(JetGood_hadronFlavour)==5)>=1")

histo_0b.Draw()
histo_1pb.Draw("same")





