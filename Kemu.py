import csv, sys
from pathlib import Path

import CttPatchParser
import LocalizationParser
import PartParser
import TechTreeModding

from Filepaths import Filepaths
from Part import Part

def getLines(filepath):
    lines = []
    try:
        with open(filepath, "r", encoding="UTF-8") as currentFile:
            for line in currentFile.readlines():
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"\033[93mgetLines(): [{filepath}] not found.\033[0m")
    except UnicodeDecodeError:
        print(f"\033[93mgetLines(): Invalid file format.\033[0m")
    return lines

def createCsv(filename, columnNames, rows):
    with open(filename, 'w', encoding="UTF-8", newline="") as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(columnNames)
        csvWriter.writerows(rows)

def generateCsvForTechTreePatch(directoryName, csvData):
    columnNames = ["Title", "Category", "Name", "Tech Node", "Tech Tier"]
    createCsv(f"ForTechTreePatch_{directoryName}.csv", columnNames, csvData)

def getCsvData(filepath):
    if not Path(filepath).exists():
        print(f"ERROR: File \"{filepath}\" does not exist.")
        sys.exit()
    csvData = []
    with open(filepath) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            csvData.append(row)
    return csvData

def getParts(directoryName, partCfgFilepaths, localizationDict):
    parts = []
    for i in range(len(partCfgFilepaths)):
        partDict = PartParser.getPartDict(getLines(partCfgFilepaths[i]))
        part = Part(directoryName, partDict, localizationDict)
        parts.append(part)
    return parts

def getAllPartData(gamedataPath, directoryName):
    fp = Filepaths(gamedataPath, directoryName)
    partCfgFilepaths = fp.partCfgFilepaths
    localizationDict = LocalizationParser.getLocalizationDict(fp.localizationPath)
    parts = getParts(directoryName, partCfgFilepaths, localizationDict)
    if fp.cttPatchFilepath != Path():
        cttPatchDict = CttPatchParser.getCttPatchDict(getLines(fp.cttPatchFilepath))
        for part in parts:
            TechTreeModding.updatePartWithCttPatch(part, cttPatchDict)
    return parts

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
# directoryName = "FarFutureTechnologies"
directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

techTierData = getCsvData("kttTechTiers.csv")

fft = getAllPartData(gamedataPath, directoryName)
fftCsvData = TechTreeModding.generateTechTreeCsvData(fft, techTierData)
generateCsvForTechTreePatch(directoryName, fftCsvData)







