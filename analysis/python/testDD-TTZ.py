from StopsDilepton.analysis.region import region
from StopsDilepton.analysis.setup import setup
#regionTTZ = getRegionsFromThresholds('dl_mt2ll', [0])  ##intention was to not use this stupid func outside. 

from StopsDilepton.analysis.DataDrivenTTZEstimate import DataDrivenTTZEstimate
setup.verbose = True

estimateTTZ = DataDrivenTTZEstimate(name='TTZ-DD', cacheDir=None)

regionTTZ = region('dl_mt2ll', (0,-1))

for channel in ['MuMu','EE','EMu']:
  res = estimateTTZ.cachedEstimate(regionTTZ,channel,setup)
  print "\n Result in ", channel," for estimate ", estimateTTZ.name, regionTTZ,":", res#, 'jer',jer, 'jec', jec