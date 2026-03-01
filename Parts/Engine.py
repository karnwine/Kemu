import CfgParser
from Parts.Part import Part

class Engine(Part):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.maxThrust = self.getMaxThrust()
        self.isp = self.getIsp()
        self.gimbal = self.getGimbal()

    def getMaxThrust(self):
        return CfgParser.getValueFromKey("maxThrust", self.partDict)

    def getIspCurve(self):
        return CfgParser.getValueFromKey("atmosphereCurve", self.partDict)

    def getIspValue(self, ispCurve, atmValue):
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
        ispCurve = self.getIspCurve()
        isp["SeaLevel"] = self.getIspValue(ispCurve, "1")
        isp["Vacuum"] = self.getIspValue(ispCurve, "0")
        return self.checkForNoneValueInIsp(isp)

    def updateIsp(self, newIspCurve):
        newIsp = {}
        newIsp["SeaLevel"] = self.getIspValue(newIspCurve, "1")
        newIsp["Vacuum"] = self.getIspValue(newIspCurve, "0")
        self.isp =self.checkForNoneValueInIsp(newIsp)

    def getGimbal(self):
        return CfgParser.getValueFromKey("gimbalRange", self.partDict)
