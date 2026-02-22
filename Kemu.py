import csv, sys
from pathlib import Path

import LocalizationParser
import PartCreator
import PartParser
import PatchParser
import TechTreeModding

from Filepaths import Filepaths

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

        # maybe remove later - useful for debugging
        partDict['PATH'] = filepath

        partDicts.append(partDict)

    return partDicts

def getAllParts(directoryName):
    filepaths = Filepaths(gamedataPath, directoryName)
    localizationDict = LocalizationParser.getLocalizationDict(getLines(filepaths.localizationPath))
    partDicts = getPartDicts(filepaths.partCfgFilepaths)
    parts = []

    for partDict in partDicts:
        part = PartCreator.createPart(directoryName, partDict, localizationDict)
        parts.append(part)

    if filepaths.cttPatchFilepath != Path():
        cttPatchDict = PatchParser.getPatchDict(getLines(filepaths.cttPatchFilepath))
        parts = TechTreeModding.updatePartsForNewTech(parts, cttPatchDict)

    return parts

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = getCsvData("kttTechTiers.csv")

nfaParts = getAllParts("NearFutureAeronautics")
nflvParts = getAllParts("NearFutureLaunchVehicles")
ceParts = getAllParts("CryoEngines")
ctParts = getAllParts("CryoTanks")
fftParts = getAllParts("FarFutureTechnologies")
stockParts = getAllParts("Squad/Parts")
mhParts = getAllParts("SquadExpansion/MakingHistory/Parts")
bgParts = getAllParts("SquadExpansion/Serenity/Parts")

cttPatchDict = PatchParser.getPatchDict(getLines("testPatch.cfg"))
for key, value in cttPatchDict.items():
    print(f"{key}: {value}\n")


# TechTreeModding.createCsvForTechTreePatch(nfaParts, techTierData)

### User modifies CSV here ###

# nfaNewTechDict = TechTreeModding.getNewTechDictFromCsv("ForTechTreePatch_NearFutureAeronautics.csv")
# nfaParts = TechTreeModding.updatePartsForNewTech(nfaParts, nfaNewTechDict)
# TechTreeModding.createTechTreePatch(nfaParts, techTierData)


