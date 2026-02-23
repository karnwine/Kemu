import CfgParser
from Parts.Part import Part

class FuelTank(Part):

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
