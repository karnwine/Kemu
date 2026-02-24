import CfgParser
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SolidEngine import SolidEngine
from Parts.RcsThruster import RcsThruster
from Parts.FuelTank import FuelTank

def isEngine(partDict):
    return CfgParser.getValueFromKey("maxThrust", partDict) != None

def isJetEngine(partDict):
    return CfgParser.getValueFromKey("velCurve", partDict) != None

def isSolidEngine(partDict):
    resources = CfgParser.getNodeDicts("RESOURCE", partDict)
    for resource in resources:
        if "SolidFuel" in resource.values():
            return True
    return False

def isPod(partDict):
    return CfgParser.getValueFromKey("category", partDict) == "Pods"

def isRcsThruster(partDict):
    hasThrusterPower = CfgParser.getValueFromKey("thrusterPower", partDict) != None
    return hasThrusterPower and not isPod(partDict)

def isFuelTank(partDict):
    hasTankCategory = CfgParser.getValueFromKey("category", partDict) == "FuelTank"
    hasPropCategory = CfgParser.getValueFromKey("category", partDict) == "Propulsion" and not isEngine(partDict)
    hasResources = CfgParser.getNodeDicts("RESOURCE", partDict) != []
    return (hasTankCategory or hasPropCategory) and hasResources

def createPart(directoryName, partDict, localizationDict):
    if isJetEngine(partDict):
        return JetEngine(directoryName, partDict, localizationDict)
    if isSolidEngine(partDict):
        return SolidEngine(directoryName, partDict, localizationDict)
    if isEngine(partDict):
        return Engine(directoryName, partDict, localizationDict)
    if isRcsThruster(partDict):
        return RcsThruster(directoryName, partDict, localizationDict)
    if isFuelTank(partDict):
        return FuelTank(directoryName, partDict, localizationDict)
    return Part(directoryName, partDict, localizationDict)

