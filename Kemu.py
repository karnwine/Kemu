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

import csv, io

def getTechDataFromCsv(filepath):
    techData = []
    with open(filepath, 'r', encoding="UTF-8") as csvfile:
        csvReader = csv.reader(csvfile)
        next(csvReader)
        for row in csvReader:
            title = row[0]
            name = row[3]
            tech = row[4]
            tier = row[5]
            techData.append((title, name, tech, tier))
    return techData

def createTechTreePatch(modName, techData):
    with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
        for item in techData:
            file.write(f"@PART[{item[1]}]:AFTER[{modName}] // {item[0]}\n")
            file.write("{\n")
            file.write(f"\t@TechRequired = {item[2]} // Tier {item[3]}\n")
            file.write("}\n")

hcData = getTechDataFromCsv(r"D:\Coding\Python\Kemu\heatControl.csv")
createTechTreePatch("HeatControl", hcData)