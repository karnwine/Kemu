import CfgParser
import EnginePatcher
import LocalizationParser
import PartCreator
import PartModding

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

def getParts(directoryName):
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
        parts = PartModding.updatePartsForNewTech(parts, cttPatchDict)

    return parts

def getAllParts(directoryNames):
    allParts = []
    for directoryName in directoryNames:
        parts = getParts(directoryName)
        allParts.extend(parts)
    return allParts

def getPartPatches(directoryName):
    return Files(gamedataPath, directoryName).partPatchFilepaths

def listPartPatches(directoryName):
    patchFilepaths = getPartPatches(directoryName)
    for path in patchFilepaths:
        print(path)

def indexPartPatches(directoryName):
    patchFilepaths = getPartPatches(directoryName)
    for index, path in enumerate(patchFilepaths):
        path = str(path)
        subStr = path.find("GameData") + 9
        path = path[subStr:]
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

def generateTechTreeCSVs(directoryNames):
    for directoryName in directoryNames:
        parts = getParts(directoryName)
        PartModding.createCsvForTechTreePatch(parts, techTierData)



gamedataPath = "D:\\Game Files\\Kerbal Space Program\\testKSP\\Kerbal Space Program\\GameData"
# gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

directoryNames = {0: "CryoEngines",
                  1: "CryoTanks",
                  2: "FarFutureTechnologies",
                  3: "HeatControl",
                  4: "KerbalAtomics",
                  5: "KerbalismConfig",
                  6: "MarkIVSystem",
                  7: "NearFutureAeronautics",
                  8: "NearFutureConstruction",
                  9: "NearFutureElectrical",
                  10: "NearFutureExploration",
                  11: "NearFutureLaunchVehicles",
                  12: "NearFuturePropulsion",
                  13: "NearFutureSolar",
                  14: "NearFutureSpacecraft",
                  15: "ReStockPlus",
                  16: "SCANsat",
                  17: "SpaceDust",
                  18: "StationPartsExpansionRedux",
                  19: "SystemHeat",
                  20: "Squad/Parts",
                  21: "SquadExpansion/MakingHistory/Parts",
                  22: "SquadExpansion/Serenity/Parts"}

mod = directoryNames[15]
parts = getParts(mod)
PartModding.createCsvForEngineBalancing("ReStockPlus", parts, techTierData)


