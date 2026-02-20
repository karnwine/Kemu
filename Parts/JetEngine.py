import PartParser
from Parts.Engine import Engine

class JetEngine(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        # self.maxThrust = self.getMaxThrustJet()
        # self.ispAsl = self.getIspJet("1")
        # self.ispVac = self.getIspJet("0")

    def getEngineModules(self):
        engineModules = []
        modules = self.locateModules()
        for module in modules:
            if "maxThrust" in module:
                engineModules.append(module)
        return engineModules

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
        return maxThrust


    # def getMaxThrustJet(self):
    #     if self.countEngineModules() == 1:
    #         return self.getMaxThrustJetSingle()

    #     maxThrust = {}
    #     for engineModule in self.getEngineModules():



    #     # maxThrust = {}
    #     # for engineModule in self.getEngineModules():
    #     #     engineId = self.getEngineModuleId(engineModule)
    #     #     key = f"MaxThrust_{engineId}"
    #     #     value = PartParser.getValueFromKey("maxThrust", engineModule)
    #     #     if Engine.isJetModule(engineModule):

    #     #     maxThrust[key] = value
    #     # return maxThrust

    # def getIsp(self, atmValue):
    #     if self.countEngineModules() == 1:
    #         return self.getIspSingle(atmValue)

    #     isp = {}
    #     atmLabel = "SeaLevel" if atmValue == "1" else "Vacuum"
    #     for engineModule in self.getEngineModules():
    #         engineId = self.getEngineModuleId(engineModule)
    #         key = f"Isp_{engineId}_{atmLabel}"
    #         value = self.getIspSingle(atmValue)
    #         isp[key] = value
    #     return isp