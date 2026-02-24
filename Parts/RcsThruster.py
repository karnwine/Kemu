import CfgParser
from Parts.Engine import Engine

class RcsThruster(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getThrusterPower()

    def getThrusterPower(self):
        return CfgParser.getValueFromKey("thrusterPower", self.partDict)