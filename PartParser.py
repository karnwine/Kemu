def parseLine(line):
    key = line.split("=")[0].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getKeyName(keyName, partDict):
    if keyName not in partDict:
        return keyName
    keyCount = len([key for key in partDict.keys() if key.startswith(keyName)]) + 1
    return f"{keyName}_{keyCount}"

def getPartDictRecursively(lines):
    partDict = {}
    lastPotentialNodeName = ""
    for line in lines:
        if line.startswith("//") or line.strip() == "":
            continue
        elif "{" in line:
            node = getPartDictRecursively(lines)
            nodeName = getKeyName(lastPotentialNodeName, partDict)
            partDict[nodeName] = node
        elif "}" in line:
            break
        elif "=" in line:
            key, value = parseLine(line)
            key = getKeyName(key, partDict)
            partDict[key] = value
        else:
            lastPotentialNodeName = line.strip()
    return partDict

def unwrapPartDictTopLevel(partDict):
    topLevelPartKey = [k for k in partDict.keys()][0]
    if "PART" not in topLevelPartKey:
        print(f"\033[93munwrapPartDictTopLevel(): WARNING - Unexpected top-level key \"{topLevelPartKey}\".\033[0m")
        return partDict
    return partDict[topLevelPartKey]

def getPartDict(lines):
    linesGenerator = (line for line in lines)
    partDict = getPartDictRecursively(linesGenerator)
    partDict = unwrapPartDictTopLevel(partDict)
    return partDict

def getValueFromKey(keyName, partDict):
    for key, value in partDict.items():
        if key == keyName:
            return value
        elif isinstance(value, dict):
            result = getValueFromKey(keyName, value)
            if result is not None:
                return result
    return None