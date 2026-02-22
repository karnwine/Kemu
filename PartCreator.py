import CfgParser
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SolidEngine import SolidEngine

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

# def isFuelTank(partDict):
#     hasTankCategory = PartParser.getValueFromKey("category", partDict) == "FuelTank"
#     # hasPropCategory = PartParser.getValueFromKey("category", partDict) == "Propulsion" and not isEngine(partDict)
#     return hasTankCategory #or hasPropCategory

def createPart(directoryName, partDict, localizationDict):
    if isJetEngine(partDict):
        return JetEngine(directoryName, partDict, localizationDict)
    if isSolidEngine(partDict):
        return SolidEngine(directoryName, partDict, localizationDict)
    if isEngine(partDict):
        return Engine(directoryName, partDict, localizationDict)
    # if isFuelTank(partDict):
    #     return FuelTank(directoryName, partDict, localizationDict)
    return Part(directoryName, partDict, localizationDict)

