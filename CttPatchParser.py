def getPartInCttPatch(lines, startingLine):
    for line in lines[startingLine:]:
        if "@PART" in line:
            line = line.split(":")[0]
            line = line.split("]")[0]
            line = line.split("[")[1]
            return line

def getTechInCttPatch(lines, startingLine):
    for line in lines[startingLine:]:
        if "@TechRequired" in line:
            line = line.split("=")[1]
            line = line.split("//")[0].strip()
            return line

def getCttPatchDict(cttPatchLines):
    if cttPatchLines == None:
        return None
    cttPatchData = {}
    lineNumber = 0
    for line in cttPatchLines:
        if "@PART" in line:
            part = getPartInCttPatch(cttPatchLines, lineNumber)
            tech = getTechInCttPatch(cttPatchLines, lineNumber)
            cttPatchData[part] = tech
        lineNumber += 1
    return cttPatchData
