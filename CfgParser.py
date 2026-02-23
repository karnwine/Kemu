def parseLine(line):
    key = line.split("=")[0].strip()
    if "@" in key:
        key = key.split("@")[1].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getKeyName(keyName, cfgDict):
    if keyName not in cfgDict:
        return keyName
    keyCount = len([key for key in cfgDict.keys() if key.startswith(keyName)]) + 1
    return f"{keyName}_{keyCount}"

def getCfgDictRecursively(lines):
    cfgDict = {}
    lastPotentialNodeName = ""
    for line in lines:
        if line.startswith("//") or line.startswith("!") or line.strip() == "":
            continue
        elif "{" in line:
            nodeName = getKeyName(lastPotentialNodeName, cfgDict)
            node = getCfgDictRecursively(lines)
            cfgDict[nodeName] = node
        elif "}" in line:
            break
        elif "=" in line:
            key, value = parseLine(line)
            key = getKeyName(key, cfgDict)
            cfgDict[key] = value
        else:
            lastPotentialNodeName = line.strip()
    return cfgDict

def unwrapPartDictTopLevel(cfgDict):
    topLevelPartKey = [k for k in cfgDict.keys()][0]
    if "PART" not in topLevelPartKey:
        return {}
    return cfgDict[topLevelPartKey]

def getPartDict(lines):
    linesGenerator = (line for line in lines)
    partDict = getCfgDictRecursively(linesGenerator)
    return unwrapPartDictTopLevel(partDict)

def getPatchDict(lines):
    linesGenerator = (line for line in lines)
    return getCfgDictRecursively(linesGenerator)

def getValueFromKey(keyName, cfgDict):
    for key, value in cfgDict.items():
        if key == keyName:
            return value
        elif isinstance(value, dict):
            result = getValueFromKey(keyName, value)
            if result is not None:
                return result

def getNodeDicts(nodeName, cfgDict):
        nodeDicts = []
        index = 2
        first = True
        while True:
            if first:
                first = False
                nodeDict = getValueFromKey(nodeName, cfgDict)
                if nodeDict == None:
                    break
                nodeDicts.append(nodeDict)
                continue
            nodeDict = getValueFromKey(f"{nodeName}_{index}", cfgDict)
            if nodeDict == None:
                break
            nodeDicts.append(nodeDict)
            index += 1
        return nodeDicts

def getAllModules(cfgDict):
    return getNodeDicts("MODULE", cfgDict)

def getSpecificModules(cfgDict, searchTerm):
        specificModules = []
        modules = getAllModules(cfgDict)
        for module in modules:
            if searchTerm in module:
                specificModules.append(module)
        return specificModules

