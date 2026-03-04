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
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

directoryNames = {0: "Squad/Parts",
                  1: "SquadExpansion/MakingHistory/Parts",
                  2: "SquadExpansion/Serenity/Parts",
                  3: "ReStockPlus",
                  4: "MarkIVSystem",
                  5: "NearFutureAeronautics",
                  6: "NearFutureConstruction",
                  7: "NearFutureExploration",
                  8: "NearFutureLaunchVehicles",
                  9: "NearFuturePropulsion",
                  10: "NearFutureSolar",
                  11: "NearFutureSpacecraft",
                  12: "HeatControl",
                  13: "SCANsat",
                  14: "StationPartsExpansionRedux",}

allParts = getAllParts(directoryNames.values())

panelList = []
for part in allParts:
    partList = []
    if "panel" in part.name.lower():
        partList.append(part.title)
        partList.append(part.mod)
        partList.append(part.path)
        partList.append(part.name)
        partList.append(part.category)
        partList.append(CfgParser.getValueFromKey("mass", part.partDict))
        panelList.append(partList)

import csv

def createCsv(filename, columnNames, rows):
    with open(filename, 'w', encoding="UTF-8", newline="") as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(columnNames)
        csvWriter.writerows(rows)

for part in allParts:
    if "battery" in part.name.lower():
        print(part.title)
        print(part.cost)


