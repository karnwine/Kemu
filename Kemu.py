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

def getAllParts(directoryName):
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

def getPartPatches(directoryName):
    return Files(gamedataPath, directoryName).partPatchFilepaths

def listPartPatches(directoryName):
    patchFilepaths = getPartPatches(directoryName)
    for index, path in enumerate(patchFilepaths):
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

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/KSP Temp/GameData"

techTierData = Files.getCsvData("kttTechTiers.csv")

ceParts = getAllParts("CryoEngines")
ctParts = getAllParts("CryoTanks")
fftParts = getAllParts("FarFutureTechnologies")
hcParts = getAllParts("HeatControl")
kaParts = getAllParts("KerbalAtomics")
kerbParts = getAllParts("KerbalismConfig")    # ctt patch needs manual parsing
m4Parts = getAllParts("MarkIVSystem")
nfaParts = getAllParts("NearFutureAeronautics")
nfcParts = getAllParts("NearFutureConstruction")
nfelParts = getAllParts("NearFutureElectrical")
nfexParts = getAllParts("NearFutureExploration")
nflvParts = getAllParts("NearFutureLaunchVehicles")
nfpParts = getAllParts("NearFuturePropulsion")
nfsolParts = getAllParts("NearFutureSolar")
nfscParts = getAllParts("NearFutureSpacecraft")
rsPlusParts = getAllParts("ReStockPlus")
scanParts = getAllParts("SCANsat")
sdParts = getAllParts("SpaceDust")
sspxParts = getAllParts("StationPartsExpansionRedux")
shParts = getAllParts("SystemHeat")
stockParts = getAllParts("Squad/Parts")
stockExMhParts = getAllParts("SquadExpansion/MakingHistory/Parts")
stockExBgParts = getAllParts("SquadExpansion/Serenity/Parts")

PartModding.createCsvForTechTreePatch(ceParts, techTierData)
PartModding.createCsvForTechTreePatch(ctParts, techTierData)
PartModding.createCsvForTechTreePatch(fftParts, techTierData)
PartModding.createCsvForTechTreePatch(hcParts, techTierData)
PartModding.createCsvForTechTreePatch(kaParts, techTierData)
PartModding.createCsvForTechTreePatch(kerbParts, techTierData)
PartModding.createCsvForTechTreePatch(m4Parts, techTierData)
PartModding.createCsvForTechTreePatch(nfaParts, techTierData)
PartModding.createCsvForTechTreePatch(nfcParts, techTierData)
PartModding.createCsvForTechTreePatch(nfelParts, techTierData)
PartModding.createCsvForTechTreePatch(nfexParts, techTierData)
PartModding.createCsvForTechTreePatch(nflvParts, techTierData)
PartModding.createCsvForTechTreePatch(nfpParts, techTierData)
PartModding.createCsvForTechTreePatch(nfsolParts, techTierData)
PartModding.createCsvForTechTreePatch(nfscParts, techTierData)
PartModding.createCsvForTechTreePatch(rsPlusParts, techTierData)
PartModding.createCsvForTechTreePatch(scanParts, techTierData)
PartModding.createCsvForTechTreePatch(sdParts, techTierData)
PartModding.createCsvForTechTreePatch(sspxParts, techTierData)
PartModding.createCsvForTechTreePatch(shParts, techTierData)
PartModding.createCsvForTechTreePatch(stockParts, techTierData)
PartModding.createCsvForTechTreePatch(stockExMhParts, techTierData)
PartModding.createCsvForTechTreePatch(stockExBgParts, techTierData)