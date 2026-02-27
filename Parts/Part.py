import CfgParser
import LocalizationParser

class Part:

    def __init__(self, directoryName, partDict, localizationDict):
        self.partDict = partDict
        self.path = self.getPath()
        self.name = ""
        self.mod = self.getMod(directoryName)
        self.category = ""
        self.title = self.getTitle(localizationDict)
        self.size = self.getSize()
        self.tech = ""
        self.cost = ""
        self.resources = self.getResources()
        self.getPartStats()

    def getPath(self):
        path = str(self.partDict.get("PATH"))
        path = path.lower()
        if "\\" in path:
            path = path.replace("\\", "/")
        subStr = path.find("parts/") + 5
        path = path[subStr:]
        return path

    def getMod(self, directoryName):
        if "makinghistory" in directoryName.lower():
            return "MakingHistory"
        if "serenity" in directoryName.lower():
            return "BreakingGround"
        if "squad" in directoryName.lower():
            return "Stock"
        return directoryName

    def getTitle(self, localizationDict):
        title = CfgParser.getValueFromKey("title", self.partDict)
        title = LocalizationParser.lookupLocalization(title, localizationDict)
        return title

    def convertSize(self, size):
        size = size.strip()
        match size:
            case "size0":
                return "0.625m"
            case "size1":
                return "1.25m"
            case "size1p5":
                return "1.875m"
            case "size2":
                return "2.5m"
            case "size3":
                return "3.75m"
            case "size4":
                return "5m"
            case _:
                return size

    def getSize(self):
        size = CfgParser.getValueFromKey("bulkheadProfiles", self.partDict)
        if size == None:
            return "bulkheadProfile(s) not found"
        size = size.split(",")
        convertedSize = []

        for s in size:
            s = self.convertSize(s)
            convertedSize.append(s)

        if len(convertedSize) == 1:
            return convertedSize[0]

        return convertedSize

    def getResources(self):
        return CfgParser.getNodeDicts("RESOURCE", self.partDict)

    def getPartStats(self):
        self.name = CfgParser.getValueFromKey("name", self.partDict)
        self.category = CfgParser.getValueFromKey("category", self.partDict)
        self.tech = CfgParser.getValueFromKey("TechRequired", self.partDict)
        self.cost = CfgParser.getValueFromKey("cost", self.partDict)
