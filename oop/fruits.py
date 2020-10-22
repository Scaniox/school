
# classes -----------------------------------------------------------------------------------------
class Fruit():
    def __init__(self, colour="unknown", size="unknown", taste="unknown"):
        self.colour = colour
        self.size = size
        self.taste = taste


    def print_description(self):
        print(f"fruit:\n    colour: {self.colour}\n     size: {self.size}\n     taste: {self.taste}")


    def __repr__(self):
        return (f"""
fruit:
    colour: {self.colour}
    size: {self.size}
    taste: {self.taste}""")



class Tropical(Fruit):
    def __init__(self, colour, size):
        super().__init__(colour, size, "Sweet")



class Citrus(Fruit):
    def __init__(self, colour="unknown", size="unknown", bitter_level=0):
        super().__init__(colour, size, "Bitter")
        self.Bitter_level = "bitter_level"


# main execution ----------------------------------------------------------------------------------
mango = Tropical("Red", "Medium")
print(mango)

lemon = Citrus("Yellow", "Small", 8)
print(lemon)
