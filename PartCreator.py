import PartParser
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SolidEngine import SolidEngine

def isEngine(partDict):
    return PartParser.getValueFromKey("maxThrust", partDict) != None

def isJetEngine(partDict):
    return PartParser.getValueFromKey("velCurve", partDict) != None

def isSolidEngine(partDict):
    resources = PartParser.getNestedDicts("RESOURCE", partDict)
    for resource in resources:
        if "SolidFuel" in resource.values():
            return True
    return False

def createPart(directoryName, partDict, localizationDict):
    if isJetEngine(partDict):
        return JetEngine(directoryName, partDict, localizationDict)
    if isSolidEngine(partDict):
        return SolidEngine(directoryName, partDict, localizationDict)
    if isEngine(partDict):
        return Engine(directoryName, partDict, localizationDict)
    return Part(directoryName, partDict, localizationDict)

