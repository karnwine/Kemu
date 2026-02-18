def getLocalizationDict(localizationFileLines):
    localizationDict = {}
    for line in localizationFileLines:
        if "=" in line:
            key = line.split("=")[0].strip()
            value = line.split("=")[1].strip()
            value = value.split("//")[0].strip()
            localizationDict[key] = value
    return localizationDict

def lookupLocalization(value, localizationDict):
    for key in localizationDict.keys():
        if value == key:
            return localizationDict[key]
    return f"\"{value}\" not found in localization file."