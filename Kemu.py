import CfgParser
import EnginePatcher
import LocalizationParser
import PartCreator
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
    files = Files(gamedataPath, directoryName)
    localizationLines = Files.getLines(files.localizationPath)
    localizationDict = LocalizationParser.getLocalizationDict(localizationLines)
    partDicts = getPartDicts(files.partCfgFilepaths)
    parts = []

    for partDict in partDicts:
        part = PartCreator.createPart(directoryName, partDict, localizationDict)
        parts.append(part)

    if files.cttPatchFilepath != None:
        cttPatchLines = Files.getLines(files.cttPatchFilepath)
        cttPatchDict = CfgParser.getPatchDict(cttPatchLines)
        parts = TechTreeModding.updatePartsForNewTech(parts, cttPatchDict)

    return parts

def getPartPatches(directoryName):
    return Files(gamedataPath, directoryName).partPatchFilepaths

def listPartPatches(directoryName):
    patchFilepaths = getPartPatches(directoryName)
    for index, path in enumerate(patchFilepaths):
        print(f"{index:02} {path}")

def applyEnginePatch(engines, patchFilePaths, patchNumber):
    patchLines = Files.getLines(patchFilePaths[patchNumber])
    patchDict = CfgParser.getPatchDict(patchLines)
    for engine in engines:
        enginePatch = EnginePatcher.getPatchDictForEngine(engine, patchDict)
        if enginePatch != None:
            if engine.__class__.__name__ == "RcsThruster":
                engine.maxThrust = EnginePatcher.getNewThrusterPower(enginePatch)
            else:
                engine.maxThrust = EnginePatcher.getNewMaxThrust(enginePatch)
            newIspCurve = EnginePatcher.getNewIspCurve(enginePatch)
            engine.updateIsp(newIspCurve)

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

# cePatches = getPartPatches("CryoEngines")
# listPartPatches("CryoEngines")



