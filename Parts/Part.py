import LocalizationParser
import PartParser

class Part:

    def __init__(self, directoryName, partDict, localizationDict):
        self.partDict = partDict
        self.name = ""
        self.mod = self.getMod(directoryName)
        self.category = ""
        self.title = self.getTitle(localizationDict)
        self.tech = ""
        self.cost = ""
        self.getPartStats()

    def getMod(self, directoryName):
        if "makinghistory" in directoryName.lower():
            return "MakingHistory"
        if "serenity" in directoryName.lower():
            return "BreakingGround"
        if "squad" in directoryName.lower():
            return "Stock"
        return directoryName

    def getTitle(self, localizationDict):
        title = PartParser.getValueFromKey("title", self.partDict)
        title = LocalizationParser.lookupLocalization(title, localizationDict)
        return title

    def getPartStats(self):
        self.name = PartParser.getValueFromKey("name", self.partDict)
        self.category = PartParser.getValueFromKey("category", self.partDict)
        self.tech = PartParser.getValueFromKey("TechRequired", self.partDict)
        self.cost = PartParser.getValueFromKey("cost", self.partDict)
