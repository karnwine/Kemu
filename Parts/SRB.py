import PartParser
from Parts.Engine import Engine

class SRB(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.solidFuel = self.getSolidFuel()

    def getSolidFuel(self):
        resourceModules = self.getSpecificModules("RESOURCE")
        for resourceModule in resourceModules:
            if "SolidFuel" in resourceModule.values():
                return PartParser.getValueFromKey("amount", resourceModule)
        return "SolidFuel Not Found"