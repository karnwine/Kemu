import csv, os, sys
from pathlib import Path

class Files:

    modPath = None
    localizationPath = None
    cttPatchFilepath = None
    cfgFilepaths = []
    partCfgFilepaths = []
    partPatchFilepaths = []

    def __init__(self, gamedataPath, directoryName):
        self.modPath = self.getModPath(gamedataPath, directoryName)
        self.localizationPath = self.getLocalizationPath(gamedataPath, directoryName)
        self.cfgFilepaths = self.getCfgFilepaths(self.modPath)
        self.cttPatchFilepath = self.getCttPatchFilepath(directoryName, self.cfgFilepaths)
        self.partCfgFilepaths = self.getPartCfgFilepaths(self.cfgFilepaths)
        self.partPatchFilepaths = self.getPartPatchFilepaths(self.cfgFilepaths)

    @staticmethod
    def getLines(filepath):
        lines = []
        try:
            with open(filepath, "r", encoding="UTF-8") as currentFile:
                for line in currentFile.readlines():
                    lines.append(line.strip())
        except Exception:
            print(f"Error reading file lines: {filepath}")
            # sys.exit()
        return lines

    @staticmethod
    def getCsvData(filepath):
        csvData = []
        with open(filepath) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                csvData.append(row)
        return csvData

    def getModPath(self, gamedataPath, directoryName):
        modPath = Path(gamedataPath) / Path(directoryName)
        if not modPath.exists():
            print("Mod filepath does not exist.")
            sys.exit()
        return modPath

    def getLocalizationPath(self, gamedataPath, directoryName):
        if directoryName == "Squad/Parts" or directoryName == "SquadExpansion/MakingHistory/Parts":
            localizationPath = Path(gamedataPath) / Path("Squad/Localization/dictionary.cfg")
        elif directoryName == "SquadExpansion/Serenity/Parts":
            localizationPath = Path(gamedataPath) / Path("SquadExpansion/Serenity/Localization/dictionary.cfg")
        elif directoryName == "SCANsat":
            localizationPath = Path(gamedataPath) / Path("SCANsat/Resources/Localization/en-us/Parts.cfg")
        else:
            localizationPath =Path(gamedataPath) / Path(f"{directoryName}/Localization/en-us.cfg")
        if not localizationPath.exists():
            print("Warning: Could not find localization file.")
        return localizationPath

    def getCfgFilepaths(self, modPath):
        cfgFilepaths = []
        for root, _, files in os.walk(modPath):
            for file in files:
                if ".cfg" in file:
                    cfgFilepaths.append(os.path.join(root,file))
        if not cfgFilepaths:
            print("No .cfg files found in directory.")
            sys.exit()
        return cfgFilepaths

    def getCttPatchFilepath(self, directoryName, cfgFilepaths):
        directoryName = directoryName.lower()
        if "squad" in directoryName or "squadexpansion" in directoryName:
            return None
        for filepath in cfgFilepaths:
            checkedFilepath = filepath.lower()
            checkedFilepath = "".join(checkedFilepath.split())
            if "ctt" in checkedFilepath or "communitytechtree" in checkedFilepath:
                return Path(filepath)

    def getPartCfgFilepaths(self, cfgFilepaths):
        partCfgFilepaths = []
        for filepath in cfgFilepaths:
            checkedFilepath = filepath.lower()
            checkedFilepath = "".join(checkedFilepath.split())
            if "parts" in checkedFilepath:
                partCfgFilepaths.append(Path(filepath))
        return partCfgFilepaths

    def getPartPatchFilepaths(self, cfgFilepaths):
        partPatchFilepaths = []
        for filepath in cfgFilepaths:
            lines = Files.getLines(filepath)
            for line in lines:
                if "@PART" in line:
                    partPatchFilepaths.append(Path(filepath))
                    break
        return partPatchFilepaths