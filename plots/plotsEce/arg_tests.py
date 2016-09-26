def makeCut(cut_value,cut_string):
  print len(cut_value)
  if len(cut_value)>1 and cut_value[1]>=0:
    return   "("+cut_string+">"+str(cut_value[0])+"&&"\
            +cut_string+"<="+str(cut_value[1])+" )"
  else:
    return   "("+cut_string+">"+str(cut_value[0])+")"

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dl_mt2ll", dest="dl_mt2ll", default="(0,-1),(100,150)", type="string", action="store", help="Which SR")
parser.add_option("--dl_mt2bb", dest="dl_mt2bb", default="(0,-1)", type="string", action="store", help="Which SR")
parser.add_option("--dl_mt2blbl", dest="dl_mt2blbl", default="(0,-1)", type="string", action="store", help="Which SR")
(options, args) = parser.parse_args()
mt2ll_cuts = eval("["+options.dl_mt2ll+"]")
for mt2ll_cut in mt2ll_cuts:
  print mt2ll_cut
  print makeCut(mt2ll_cut , "dl_mt2ll")

