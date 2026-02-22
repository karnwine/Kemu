import PartParser
from Parts.Engine import Engine

class SolidEngine(Engine):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.solidFuel = self.getSolidFuel()

    def getSolidFuel(self):
        resources = PartParser.getNestedDicts("RESOURCE", self.partDict)
        for resource in resources:
            if "SolidFuel" in resource.values():
                return PartParser.getValueFromKey("amount", resource)
        return "SolidFuel Not Found"