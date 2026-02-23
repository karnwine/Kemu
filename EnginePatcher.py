import CfgParser

def parsePartName(line):
    partName = line.split(":")[0]
    partName = partName.split("@")[1]
    partName = partName.split("[")[1]
    partName = partName.split("]")[0].strip()
    return partName

def getPatchDict(engine, patchDict):
    for key, value in patchDict.items():
        if engine.name in key:
            return value
    return None

def getNewMaxThrust(enginePatchDict):
    return CfgParser.getValueFromKey("maxThrust", enginePatchDict)

def getNewIspCurve(enginePatchDict):
    return CfgParser.getValueFromKey("atmosphereCurve", enginePatchDict)


