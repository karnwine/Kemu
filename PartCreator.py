import PartParser
from Parts.Part import Part
from Parts.Engine import Engine
from Parts.JetEngine import JetEngine
from Parts.SRB import SRB

def isEngine(partDict):
    return PartParser.getValueFromKey("maxThrust", partDict) != None

def isJetEngine(partDict):
    return PartParser.getValueFromKey("velCurve", partDict) != None

def isSRB(partDict):
    resourceModules = PartParser.getSpecificModules(partDict, "RESOURCE")
    for resourceModule in resourceModules:
        if "SolidFuel" in resourceModule.values():
            return True
    return False

def createPart(directoryName, partDict, localizationDict):
    if isJetEngine(partDict):
        return JetEngine(directoryName, partDict, localizationDict)
    if isSRB(partDict):
        return SRB(directoryName, partDict, localizationDict)
    if isEngine(partDict):
        return Engine(directoryName, partDict, localizationDict)
    return Part(directoryName, partDict, localizationDict)

