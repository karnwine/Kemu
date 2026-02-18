import csv, sys
from pathlib import Path

import CttPatchParser
import LocalizationParser
import PartParser
import TechTreeModding

from Filepaths import Filepaths
from Parts.Part import Part

def getLines(filepath):
    lines = []
    RED = "\033[91m"
    RESET = "\033[0m"
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
    RED = "\033[91m"
    RESET = "\033[0m"
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
        partDicts.append(partDict)
    return partDicts

def getParts(directoryName):
    filepaths = Filepaths(gamedataPath, directoryName)
    localizationDict = LocalizationParser.getLocalizationDict(getLines(filepaths.localizationPath))
    partDicts = getPartDicts(filepaths.partCfgFilepaths)
    parts = []
    for partDict in partDicts:
        part = Part(directoryName, partDict, localizationDict)
        parts.append(part)
    if filepaths.cttPatchFilepath != Path():
        cttPatchDict = CttPatchParser.getCttPatchDict(getLines(filepaths.cttPatchFilepath))
        parts = TechTreeModding.updatePartsForNewTech(parts, cttPatchDict)
    return parts

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
# directoryName = "FarFutureTechnologies"
# directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

techTierData = getCsvData("kttTechTiers.csv")

# nfaParts = getParts("NearFutureAeronautics")
# TechTreeModding.createCsvForTechTreePatch(nfaParts, techTierData)

fftParts = getParts("FarFutureTechnologies")
# TechTreeModding.createCsvForTechTreePatch(fftParts, techTierData)

for part in fftParts:

    print(PartParser.getValueFromKey("maxThrust_2", part.partDict))


### User modifies CSV here ###

# nfaNewTechDict = TechTreeModding.getNewTechDictFromCsv("ForTechTreePatch_NearFutureAeronautics.csv")
# nfaParts = TechTreeModding.updatePartsForNewTech(nfaParts, nfaNewTechDict)
# TechTreeModding.createTechTreePatch(nfaParts, techTierData)


