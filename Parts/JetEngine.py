import PartParser
from Parts.Engine import Engine

class JetEngine(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getMaxThrustJet()
        self.isp = self.getIspJet()

    def getEngineModules(self):
        return PartParser.getSpecificModules(self.partDict, "maxThrust")

    def getEngineModuleId(self, engineModule):
        for key, value in engineModule.items():
            if key == "engineID":
                return value

    def countEngineModules(self):
        return len(self.getEngineModules())

    def getMaxVelCurveThrustMult(self, engineModule):
        velCurveThrustMult = {}
        mach = ""
        maxMult = 0
        velCurve = PartParser.getValueFromKey("velCurve", engineModule)

        for value in velCurve.values():
            mult = float(value.split(" ")[1].strip())
            if mult > maxMult:
                mach = value.split(" ")[0].strip()
                maxMult = mult

        velCurveThrustMult[mach] = maxMult

        return velCurveThrustMult

    def getMaxThrustJetSingle(self):
        engineModule = self.getEngineModules()[0]
        velCurveThrustMult = self.getMaxVelCurveThrustMult(engineModule)
        velCurveThrustMult = list(velCurveThrustMult.values())[0]
        maxThrust = float(PartParser.getValueFromKey("maxThrust", engineModule))
        maxThrust *= velCurveThrustMult
        maxThrust = str(int(maxThrust))
        return maxThrust

    def getMaxThrustJet(self):
        if self.countEngineModules() == 1:
            return self.getMaxThrustJetSingle()
        
        maxThrust = {}
        for engineModule in self.getEngineModules():
            engineId = self.getEngineModuleId(engineModule)
            key = f"MaxThrust_{engineId}"
            if "velCurve" in engineModule:
                value = self.getMaxThrustJetSingle()
            else:
                value = PartParser.getValueFromKey("maxThrust", engineModule)
            maxThrust[key] = value
        return maxThrust

    def checkForDuplicateIspValues(self, ispDict):
        ispValues = list(ispDict.values())
        firstValue = ispValues[0]
        hasDuplicateValues = True
        for value in ispValues:
            if value != firstValue:
                hasDuplicateValues = False
        if hasDuplicateValues:
            return firstValue
        return ispDict

    def getIspJet(self):
        if self.countEngineModules() == 1:
            return self.getIsp()
        
        isp = {}
        for engineModule in self.getEngineModules():
            engineId = self.getEngineModuleId(engineModule)
            key = f"Isp_{engineId}"
            value = self.getIsp()
            isp[key] = value
        isp = self.checkForDuplicateIspValues(isp)
        return isp