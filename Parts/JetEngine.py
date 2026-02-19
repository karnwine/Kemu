import PartParser
from Parts.Engine import Engine

class JetEngine(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.velCurve = self.getVelCurve()
        self.maxThrust = self.getMaxJetThrust()

    def getVelCurve(self):
        return PartParser.getValueFromKey("velCurve", self.partDict)

    def getMaxVelCurveThrustMult(self):
        maxMult = 0
        for value in self.velCurve.values():
            mult = value.split(" ")[1].strip()
            if float(mult) > maxMult:
                maxMult = float(mult)
        return maxMult

    def getMaxJetThrust(self):
        maxThrust = float(PartParser.getValueFromKey("maxThrust", self.partDict))
        maxThrust *= self.getMaxVelCurveThrustMult()
        return maxThrust
