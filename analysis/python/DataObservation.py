# Logging
import logging
import os
import json
logger = logging.getLogger(__name__)

from StopsDilepton.analysis.Region import Region
from StopsDilepton.analysis.u_float import u_float
from StopsDilepton.analysis.Cache import Cache

class DataObservation():
    def __init__(self, name, sample, cacheDir=None):
        self.name = name
        self.sample=sample
        self.initCache(cacheDir)

    def initCache(self, cacheDir):
        if cacheDir:
            self.cacheDir=cacheDir
            cacheFileName = os.path.join(cacheDir, self.name+'.pkl')
            if not os.path.exists(os.path.dirname(cacheFileName)):
                os.makedirs(os.path.dirname(cacheFileName))
            self.cache = Cache(cacheFileName, verbosity=1)
        else:
            self.cache=None

    def uniqueKey(self, region, channel, setup):
        return region, channel, json.dumps(setup.sys, sort_keys=True), json.dumps(setup.parameters, sort_keys=True), json.dumps(setup.lumi, sort_keys=True)

    # alias for cachedObservation to make it easier to call the same function as for the mc's
    def cachedEstimate(self, region, channel, setup, save=True):
        return self.cachedObservation(region, channel, setup, save)

    def cachedObservation(self, region, channel, setup, save=True):
        key =  self.uniqueKey(region, channel, setup)
        if self.cache and self.cache.contains(key):
            res = self.cache.get(key)
            logger.info( "Loading cached %s result for %r : %r"%(self.name, key, res) )
            return res
        elif self.cache:
            logger.info( "Adding cached %s result for %r"%(self.name, key) )
            return self.cache.add( key, self.observation( region, channel, setup), save=save)
        else:
            return self.observation( region, channel, setup)

    def observation(self, region, channel, setup):

        if channel=='all':
            return sum([self.cachedObservation(region, c, setup) for c in ['MuMu', 'EE', 'EMu']])

        if channel=='SF':
            return sum([self.cachedObservation(region, c, setup) for c in ['MuMu', 'EE']])

        else:
            zWindow= 'allZ' if channel=='EMu' else 'offZ'

            preSelection = setup.preselection('Data', zWindow=zWindow, channel=channel)
            cut = "&&".join([region.cutString(setup.sys['selectionModifier']), preSelection['cut']])

            logger.debug( "Using cut %s"% cut )

            return u_float(**self.sample[channel].getYieldFromDraw(selectionString = cut, weightString = 'weight') )
