import csv, sys
from pathlib import Path

from CttData import CttData
from Filepaths import Filepaths
from Part import Part
import LocalizationParser
import PartParser

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

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
directoryName = "FarFutureTechnologies"
# directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

techTierData = getCsvData("kttTechTiers.csv")

filepaths = Filepaths(gamedataPath, directoryName)
partCfgFilepaths = filepaths.partCfgFilepaths
print(partCfgFilepaths[0])
parts = []
localizationDict = LocalizationParser.getLocalizationDict(filepaths.localizationPath)

for i in range(len(partCfgFilepaths)):
    partDict = PartParser.getPartDict(getLines(partCfgFilepaths[i]))
    part = Part(directoryName, partDict, localizationDict)
    parts.append(part)

num = 1
for part in parts:
    print(str(num), end=": ")
    print(f"\033[92mName: {part.name}", end=" ")
    print(f"\033[94mMod: {part.mod}\033[0m", end = " ")
    print(f"\033[93mTitle: {part.title}\033[0m")
    num += 1





