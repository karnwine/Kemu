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

def partCountCheck(parts):
    for index, part in enumerate(parts):
        print(f"{index:03} {part.title}")
    print()
    print(f"\033[92m{len(parts)} parts found in {parts[0].mod} directory.\033[0m")
    print()


# gamedataPath = "D:\\Game Files\\Kerbal Space Program\\testKSP\\Kerbal Space Program\\GameData"
# gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

directoryNames = {0: "Squad/Parts",
                  1: "SquadExpansion/MakingHistory/Parts",
                  2: "SquadExpansion/Serenity/Parts",
                  3: "ReStockPlus",
                  4: "MarkIVSystem",
                  5: "NearFutureAeronautics",
                  6: "NearFutureConstruction",
                  7: "NearFutureElectrical",
                  8: "NearFutureExploration",
                  9: "NearFutureLaunchVehicles",
                  10: "NearFuturePropulsion",
                  11: "NearFutureSolar",
                  12: "NearFutureSpacecraft",
                  13: "HeatControl",
                  14: "SCANsat",
                  15: "StationPartsExpansionRedux",}

# parts = getParts(directoryNames[20])
# PartModding.createCsvForEngineBalancing("Stock", parts, techTierData)
# PartModding.createCsvForSolidEngineBalancing("Stock", parts, techTierData)
# PartModding.createCsvForJetEngineBalancing("Stock", parts, techTierData)

generateTechTreeCSVs(list(directoryNames.values()))

# count = 0
# for part in nfelParts:
#     modules = CfgParser.getAllModules(part.partDict)

#     for module in modules:
#         for key, value in module.items():
#             if "ModuleRCSEmissive" in value:
#                 count += 1
#                 print()
#                 print(f"{part.title}")
#                 print(part.path)
# print(count)

