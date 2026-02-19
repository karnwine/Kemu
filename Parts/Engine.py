import PartParser
from Parts.Part import Part

class Engine(Part):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getMaxThrust()
        self.ispAsl = self.getIsp("1")
        self.ispVac = self.getIsp("0")

    def getMaxThrust(self):
        return PartParser.getValueFromKey("maxThrust", self.partDict)

    def getIsp(self, atmValue):
        ispCurve = PartParser.getValueFromKey("atmosphereCurve", self.partDict)
        for value in ispCurve.values():
            value = value.split(" ")
            if value[0].strip() == atmValue:
                return value[1].strip()
        return None
