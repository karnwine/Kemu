import os, sys
from pathlib import Path

class Filepaths:

    modPath = Path()
    localizationPath = Path()
    cttPatchFilepath = Path()
    cfgFilepaths = []
    partCfgFilepaths = []

    def __init__(self, gamedataPath, directoryName):
        self.modPath = self.getModPath(gamedataPath, directoryName)
        self.localizationPath = self.getLocalizationPath(gamedataPath, directoryName)
        self.cfgFilepaths = self.getCfgFilepaths(self.modPath)
        self.cttPatchFilepath = self.getCttPatchFilepath(directoryName, self.cfgFilepaths)
        self.partCfgFilepaths = self.getPartCfgFilepaths(self.cfgFilepaths)

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
        else:
            localizationPath =Path(gamedataPath) / Path(f"{directoryName}/Localization/en-us.cfg")
        if not localizationPath.exists():
            print("Could not find localization file.")
            sys.exit()
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
            return Path()
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