import CfgParser
import LocalizationParser
import PartCreator
from Parts.FuelTank import FuelTank
import TechTreeModding

from Files import Files

def getPartDicts(partCfgFilepaths):
    partDicts = []
    for filepath in partCfgFilepaths:
        partLines = Files.getLines(filepath)
        partDict = CfgParser.getPartDict(partLines)
        if partDict == {}:
            continue
        if CfgParser.getValueFromKey("TechRequired", partDict) == "Unresearcheable":
            continue
        if partDict.get("module") == None:
            continue

        val = CfgParser.getValueFromKey("TechHidden", partDict)
        if val and val.lower() == "true":
            continue

        # maybe remove later - useful for debugging
        partDict['PATH'] = filepath

        partDicts.append(partDict)

    return partDicts

def getAllParts(directoryName):
    filepaths = Files(gamedataPath, directoryName)
    localizationLines = Files.getLines(filepaths.localizationPath)
    localizationDict = LocalizationParser.getLocalizationDict(localizationLines)
    partDicts = getPartDicts(filepaths.partCfgFilepaths)
    parts = []

    for partDict in partDicts:
        part = PartCreator.createPart(directoryName, partDict, localizationDict)
        parts.append(part)

    if filepaths.cttPatchFilepath != None:
        cttPatchLines = Files.getLines(filepaths.cttPatchFilepath)
        cttPatchDict = CfgParser.getPatchDict(cttPatchLines)
        parts = TechTreeModding.updatePartsForNewTech(parts, cttPatchDict)

    return parts

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

nfaParts = getAllParts("NearFutureAeronautics")
nflvParts = getAllParts("NearFutureLaunchVehicles")
ceParts = getAllParts("CryoEngines")
ctParts = getAllParts("CryoTanks")
fftParts = getAllParts("FarFutureTechnologies")
stockParts = getAllParts("Squad/Parts")
mhParts = getAllParts("SquadExpansion/MakingHistory/Parts")
bgParts = getAllParts("SquadExpansion/Serenity/Parts")
allParts = nfaParts + nflvParts + ceParts + ctParts + fftParts + stockParts + mhParts + bgParts

# testLines = Files.getLines("testPatch.cfg")
# testPatchDict = CfgParser.getPatchDict(testLines)
# from pprint import pp
# pp(testPatchDict)