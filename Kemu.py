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
        if CfgParser.getValueFromKey("MHReplacement", partDict) != None:
            continue
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


gamedataPath = "D:\\Game Files\\Kerbal Space Program\\testKSP\\Kerbal Space Program\\GameData"
# gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

def parsePart(line):
    part = line.split("[")[1]
    return part.split("]")[0].strip()

def parseTech(line):
    tech = line.split("=")[1]
    return tech.split("//")[0].strip()

kttMainCfg = r"D:\Cloud Archive\Game Stuff\KSP\Custom Mods\TKO\_wip\kiwiTechTree-master\GameData\KiwiTechTree\Configurations\Core\Main.cfg"
kttMainCfgLines = Files.getLines(kttMainCfg)
kttMainData = []

for line in kttMainCfgLines:
    if "@PART" in line:
        part = parsePart(line)
    if "@TechRequired" in line:
        tech = parseTech(line)
        kttMainData.append((part, tech))

import csv

with open("kttMainCfg.csv", 'w', encoding="UTF-8", newline="") as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(["part name", "tech"])
    csvWriter.writerows(kttMainData)