from Parts.Part import Part

class FuelTank(Part):

    fuelNames = ["LiquidFuel", "MonoPropellant", "XenonGas", "LqdHydrogen", "LqdMethane"]

    def __init__(self, directoryName, partDict, localizationDict):
        super().__init__(directoryName, partDict, localizationDict)
        self.fuelCapacity = self.getFuelCapacity()

    def getFuelCapacity(self):
        fuelCapacity = {}
        for resource in self.resources:
            for key, value in resource.items():
                if key == "name" and value in self.fuelNames:
                    fuelCapacity[value] = resource.get("amount")
        return fuelCapacity
