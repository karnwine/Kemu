import CfgParser
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SolidEngine import SolidEngine
from Parts.FuelTank import FuelTank
from Parts.RcsThruster import RcsThruster

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

def isRcsThruster(partDict):
    hasThrusterPower = CfgParser.getValueFromKey("thrusterPower", partDict) != None
    isNotPod = CfgParser.getValueFromKey("category", partDict) != "Pods"
    return hasThrusterPower and isNotPod

def isFuelTank(partDict):
    hasTankCategory = CfgParser.getValueFromKey("category", partDict) == "FuelTank"
    hasPropCategory = CfgParser.getValueFromKey("category", partDict) == "Propulsion" and not isEngine(partDict)
    return hasTankCategory or hasPropCategory

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

