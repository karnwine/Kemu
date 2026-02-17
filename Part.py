import LocalizationParser
import PartParser

class Part:

    def __init__(self, directoryName, partDict, localizationDict):
        self.directoryName = directoryName
        self.partDict = partDict
        self.localizationDict = localizationDict
        self.name = ""
        self.mod = ""
        self.category = ""
        self.title = ""
        self.tech = ""
        self.cost = ""
        self.getBasicPartStats()

    def getMod(self):
        directoryName = self.directoryName.lower()
        if "squadexpansion" in directoryName:
            return "Stock Expansion"
        if "squad" in directoryName:
            return "Stock"
        return self.directoryName

    def getTitle(self):
        title = PartParser.getValueFromKey("title", self.partDict)
        title = LocalizationParser.lookupLocalization(title, self.localizationDict)
        return title

    def getBasicPartStats(self):
        self.name = PartParser.getValueFromKey("name", self.partDict)
        self.mod = self.getMod()
        self.category = PartParser.getValueFromKey("category", self.partDict)
        self.title = self.getTitle()
        self.tech = PartParser.getValueFromKey("TechRequired", self.partDict)
        self.cost = PartParser.getValueFromKey("cost", self.partDict)
