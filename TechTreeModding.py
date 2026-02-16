import io

class TechTreeModding:

    def __init__(self, techTierData):
        self.techTierData = techTierData

    @classmethod
    def lookupTechTreeTier(cls, techNode):
        for row in cls.techTierData:
            if row[0] == techNode:
                return row[1]
        return "TECH NODE NOT FOUND"
    
    @staticmethod
    def updatePartWithCttPatch(part, cttPatchData):
        for key, value in cttPatchData:
            if key == part.name:
                part.tech = value
                return            
        print(f"{part.name} not found in CTT Patch")            

    @classmethod
    def generateTechTreeCsvData(cls, parts):
        pass

    @classmethod
    def createTechTreePatch(cls, parts):
        pass
        # modName = parts[0].mod
        # with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
        #     for part in parts:
        #         techTier = cls.lookupTechTreeTier(part.tech)
        #         file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
        #         file.write("{\n")
        #         file.write(f"\t@techRequired = {part.tech} // Tier {techTier}\n")
        #         file.write("}\n")
