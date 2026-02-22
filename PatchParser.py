def parseNodeLine(line):
    nodeName = line.split("[")[0].strip()
    nodeName = nodeName.split("@")[1].strip()
    nodeItem = line.split("[")[1].strip()
    nodeItem = nodeItem.split("]")[0].strip()
    return nodeName, nodeItem

def parseKeyValueLine(line):
    key = line.split("=")[0].strip()
    key = key.split("@")[1].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getPatchDictRecursively(lines):
    patchDict = {}
    lastPotentialNodeName = ""
    for line in lines:
        if line.startswith("//") or line.strip() == "":
            continue
        elif "{" in line:
            node = getPatchDictRecursively(lines)
            nodeName = lastPotentialNodeName
            patchDict[nodeName] = node
        elif "}" in line:
            break
        elif "=" in line:
            key, value = parseKeyValueLine(line)
            patchDict[key] = value
        else:
            lastPotentialNodeName = line.strip()
    return patchDict

def getPatchDict(lines):
    linesGenerator = (line for line in lines)
    patchDict = getPatchDictRecursively(linesGenerator)
    return patchDict
    

    
