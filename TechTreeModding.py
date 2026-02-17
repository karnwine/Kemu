import io

def lookupTechTreeTier(techTierData, techNode):
    for row in techTierData:
        if row[0] == techNode:
            return row[1]
    return "TECH NODE NOT FOUND"

def updatePartWithCttPatch(part, cttPatchDict):
    for key, value in cttPatchDict.items():
        if key == part.name:
            part.tech = value
            return

def generateTechTreeCsvData(parts, techTierData):
    csvData = []
    for part in parts:
        techNode = part.tech
        techTier = lookupTechTreeTier(techTierData, techNode)
        csvData.append((part.title, part.category, part.name, part.tech, techTier))
    return csvData

def createTechTreePatch(parts):
    pass
    # modName = parts[0].mod
    # with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
    #     for part in parts:
    #         techTier = cls.lookupTechTreeTier(part.tech)
    #         file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
    #         file.write("{\n")
    #         file.write(f"\t@techRequired = {part.tech} // Tier {techTier}\n")
    #         file.write("}\n")
