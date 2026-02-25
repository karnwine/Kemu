import csv, io
import CfgParser
from pathlib import Path
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SolidEngine import SolidEngine

def lookupTechTreeTier(techTierData, techNode):
    for row in techTierData:
        if row[0] == techNode:
            return row[1]
    return "TECH NODE NOT FOUND"

def parseNewTechDict(newTechDict):
    parsedDict = {}
    for key, value in newTechDict.items():
        key = key.split(":")[0]
        key = key.split("@")[1]
        key = key.split("[")[1]
        key = key.split("]")[0].strip()
        value = value["TechRequired"]
        parsedDict[key] = value
    return parsedDict

def updatePartsForNewTech(parts, newTechDict):
    newTechDict = parseNewTechDict(newTechDict)
    for part in parts:
        for key in newTechDict.keys():
            if part.name == key:
                part.tech = newTechDict[key]
    return parts

def createCsv(filename, columnNames, rows):
    with open(filename, 'w', encoding="UTF-8", newline="") as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(columnNames)
        csvWriter.writerows(rows)

def generateTechTreeCsvData(parts, techTierData):
    csvData = []
    for part in parts:
        techTier = lookupTechTreeTier(techTierData, part.tech)
        csvData.append((part.title, part.category, part.name, part.tech, techTier))
    return csvData

def createCsvForTechTreePatch(parts, techTierData):
    mod = parts[0].mod
    filename = f"ForTechTreePatch_{mod}.csv"
    columnNames = ["Part Title", "Part Category", "Part Name", "Tech Node", "Tech Tier"]
    rows = generateTechTreeCsvData(parts, techTierData)
    createCsv(filename, columnNames, rows)

def generateEngineBalancingCsvData(parts, techTierData):
    csvData = []
    for part in parts:
        if not isinstance(part, Engine):
            continue
        if isinstance(part, JetEngine):
            continue

        techTier = lookupTechTreeTier(techTierData, part.tech)
        ispAsl = int(part.isp['SeaLevel'])
        ispVac = int(part.isp['Vacuum'])
        ispDiff = ispVac - ispAsl
        csvData.append((part.title, part.mod, part.name, part.cost, part.size, part.maxThrust,
                        ispAsl, ispVac, ispDiff, part.gimbal, part.tech, techTier))
    return csvData

def createCsvForEngineBalancing(parts, techTierData):
    mod = parts[0].mod
    filename = f"ForEngineBalancing_{mod}.csv"
    columnNames = ["Part Title", "Mod", "Part Name", "Cost", "Size", "Max Thrust", "Isp (ASL)",
                   "Isp (Vac)", "Isp Diff", "Gimbal Range", "Tech Node", "Tech Tier"]
    rows = generateEngineBalancingCsvData(parts, techTierData)
    createCsv(filename, columnNames, rows)

def generateSolidEngineBalancingCsvData(parts, techTierData):
    csvData = []
    for part in parts:
        if not isinstance(part, SolidEngine):
            continue

        ispAsl = part.isp['SeaLevel']
        techTier = lookupTechTreeTier(techTierData, part.tech)
        csvData.append((part.title, part.mod, part.name, part.cost, part.size,part.maxThrust,
                        part.solidFuel, ispAsl, part.gimbal, part.tech, techTier))
    return csvData

def createCsvForSolidEngineBalancing(parts, techTierData):
    mod = parts[0].mod
    filename = f"ForSolidEngineBalancing_{mod}.csv"
    columnNames = ["Part Title", "Mod", "Part Name", "Cost", "Size", "Max Thrust",
                   "Solid Fuel", "Isp (ASL)", "Gimbal Range", "Tech Node", "Tech Tier"]
    rows = generateSolidEngineBalancingCsvData(parts, techTierData)
    createCsv(filename, columnNames, rows)

def isMultimode(engine):
    return isinstance(engine.maxThrust, dict)

def generateJetEngineBalancingCsvData(parts, techTierData):
    csvData = []
    for part in parts:
        if not isinstance(part, JetEngine):
            continue
        maxThrustPrimary = list(part.maxThrust.values())[0] if isMultimode(part) else part.maxThrust
        maxThrustSecondary = list(part.maxThrust.values())[1] if isMultimode(part) else ""
        techTier = lookupTechTreeTier(techTierData, part.tech)
        csvData.append((part.title, part.mod, part.name, part.cost, part.size, maxThrustPrimary,
                        maxThrustSecondary, part.isp, part.gimbal, part.tech, techTier))
    return csvData

def createCsvForJetEngineBalancing(parts, techTierData):
    mod = parts[0].mod
    filename = f"ForJetEngineBalancing_{mod}.csv"
    columnNames = ["Part Title", "Mod", "Part Name", "Cost", "Size", "Max Thrust", "Max Thrust (Secondary)",
                   "Isp(s)", "Gimbal Range", "Tech Node", "Tech Tier",]
    rows = generateJetEngineBalancingCsvData(parts, techTierData)
    createCsv(filename, columnNames, rows)

def getNewTechDictFromCsv(filepath):
    newTechDict = {}
    with open(filepath, 'r', encoding="UTF-8") as csvfile:
        csvReader = csv.reader(csvfile)
        next(csvReader)
        for row in csvReader:
            partName = row[2]
            newTech = row[3]
            newTechDict[partName] = newTech
    return newTechDict

def createTechTreePatch(parts, techTierData):
    modName = parts[0].mod
    with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
        for part in parts:
            techTier = lookupTechTreeTier(techTierData, part.tech)
            file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
            file.write("{\n")
            file.write(f"\t@techRequired = {part.tech} // Tier {techTier}\n")
            file.write("}\n")

def createPartCostPatch(parts):
    modName = parts[0].mod
    with io.open(f"PartCostPatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
        for part in parts:
            file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
            file.write("{\n")
            file.write(f"\t@cost = {part.cost}\n")
            file.write("}\n")
