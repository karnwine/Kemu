import csv, sys
from pathlib import Path

import CttPatchParser
import LocalizationParser
import PartParser
import TechTreeModding

from Filepaths import Filepaths
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine

RED = "\033[91m"
RESET = "\033[0m"

def getLines(filepath):
    lines = []

    try:
        with open(filepath, "r", encoding="UTF-8") as currentFile:
            for line in currentFile.readlines():
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"{RED}ERROR: [{filepath}] not found.{RESET}")
    except UnicodeDecodeError:
        print(f"{RED}ERROR: Invalid file format.{RESET}")

    return lines

def getCsvData(filepath):
    if not Path(filepath).exists():
        print(f"{RED}ERROR: File \"{filepath}\" not found.{RESET}")
        sys.exit()

    csvData = []
    with open(filepath) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            csvData.append(row)

    return csvData

def getPartDicts(partCfgFilepaths):
    partDicts = []

    for filepath in partCfgFilepaths:
        partDict = PartParser.getPartDict(getLines(filepath))
        if partDict == {}:
            continue
        if PartParser.getValueFromKey("TechRequired", partDict) == "Unresearcheable":
            continue
        if partDict.get("module") == None:
            continue

        val = PartParser.getValueFromKey("TechHidden", partDict)
        if val and val.lower() == "true":
            continue

        partDicts.append(partDict)

    return partDicts

def createPart(directoryName, partDict, localizationDict):
    if PartParser.getValueFromKey("velCurve", partDict) != None:
        return JetEngine(directoryName, partDict, localizationDict)
    if PartParser.getValueFromKey("maxThrust", partDict) != None:
        return Engine(directoryName, partDict, localizationDict)
    return Part(directoryName, partDict, localizationDict)

def getAllParts(directoryName):
    filepaths = Filepaths(gamedataPath, directoryName)
    localizationDict = LocalizationParser.getLocalizationDict(getLines(filepaths.localizationPath))
    partDicts = getPartDicts(filepaths.partCfgFilepaths)
    parts = []

    for partDict in partDicts:
        part = createPart(directoryName, partDict, localizationDict)
        parts.append(part)

    if filepaths.cttPatchFilepath != Path():
        cttPatchDict = CttPatchParser.getCttPatchDict(getLines(filepaths.cttPatchFilepath))
        parts = TechTreeModding.updatePartsForNewTech(parts, cttPatchDict)

    return parts

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
# directoryName = "FarFutureTechnologies"
# directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

techTierData = getCsvData("kttTechTiers.csv")

nfaParts = getAllParts("NearFutureAeronautics")
# TechTreeModding.createCsvForTechTreePatch(nfaParts, techTierData)

# fftParts = getAllParts("FarFutureTechnologies")
# TechTreeModding.createCsvForTechTreePatch(fftParts, techTierData)

# stockParts = getAllParts("Squad/Parts")

for part in nfaParts:
    if isinstance(part, JetEngine):
        print(f"{part.name} - Isp: {part.ispVac} maxJetThrust: {part.maxThrust}")

### User modifies CSV here ###

# nfaNewTechDict = TechTreeModding.getNewTechDictFromCsv("ForTechTreePatch_NearFutureAeronautics.csv")
# nfaParts = TechTreeModding.updatePartsForNewTech(nfaParts, nfaNewTechDict)
# TechTreeModding.createTechTreePatch(nfaParts, techTierData)


