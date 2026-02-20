import PartParser
from Parts.Part import Part

class Engine(Part):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getMaxThrust()
        self.ispAsl = self.getIsp("1")
        self.ispVac = self.getIsp("0")

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

    def getMaxThrust(self):
        if self.countEngineModules() == 1:
            return PartParser.getValueFromKey("maxThrust", self.partDict)

        maxThrust = {}
        for engineModule in self.getEngineModules():
            engineId = self.getEngineModuleId(engineModule)
            key = f"MaxThrust_{engineId}"
            value = PartParser.getValueFromKey("maxThrust", engineModule)
            maxThrust[key] = value
        return maxThrust

    def getIspSingle(self, atmValue):
        ispCurve = PartParser.getValueFromKey("atmosphereCurve", self.partDict)
        for value in ispCurve.values():
            value = value.split(" ")
            if value[0].strip() == atmValue:
                return value[1].strip()

    def getIsp(self, atmValue):
        if self.countEngineModules() == 1:
            return self.getIspSingle(atmValue)

        isp = {}
        atmLabel = "SeaLevel" if atmValue == "1" else "Vacuum"
        for engineModule in self.getEngineModules():
            engineId = self.getEngineModuleId(engineModule)
            key = f"Isp_{engineId}_{atmLabel}"
            value = self.getIspSingle(atmValue)
            isp[key] = value
        return isp

