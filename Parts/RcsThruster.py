import CfgParser
from Parts.Part import Part

class RcsThruster(Part):
    
    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.thrusterPower = self.getThrusterPower()

    def getThrusterPower(self):
        return 69