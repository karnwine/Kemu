import PartParser
from Parts.Part import Part

class Engine(Part):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getMaxThrust()
        self.isp = self.getIsp()
        self.gimbal = self.getGimbal()

    def getMaxThrust(self):
        return PartParser.getValueFromKey("maxThrust", self.partDict)

    def getIspValue(self, atmValue):
        ispCurve = PartParser.getValueFromKey("atmosphereCurve", self.partDict)
        for value in ispCurve.values():
            value = value.split(" ")
            if value[0].strip() == atmValue:
                return value[1].strip()

    def checkForNoneValueInIsp(self, ispDict):
        if ispDict["SeaLevel"] == None:
            return ispDict["Vacuum"]
        if ispDict["Vacuum"] == None:
            return ispDict["SeaLevel"]
        return ispDict
            
    def getIsp(self):
        isp = {}
        isp["SeaLevel"] = self.getIspValue("1")
        isp["Vacuum"] = self.getIspValue("0")
        return self.checkForNoneValueInIsp(isp)

    def getGimbal(self):
        return PartParser.getValueFromKey("gimbalRange", self.partDict)
