from StopsDilepton.tools.m2Calculator import m2Calculator
m=m2Calculator()

for i in range(10):
    m.setBJet1(100,0,1)
    m.setBJet2(900,0.5,1)
    m.setLepton1(50,-1,1.5)
    m.setLepton2(70,-1.2,.5)
    m.setMet(30*i,0.7)
    print "Result", m.m2CC()
