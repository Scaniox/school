


class Animal():
    def __init__(self, species="uknown", age=0, threat_level="peaceful", hungar_level=0 ):
        self.species = species
        self.age = age
        self.threat_level = threat_level
        self.hungar_level = hungar_level


    def __repr__(self):
        return f"animal instance:\nspecies: {self.species}\nage: {self.age}\nthreat level:\
                {self.threat_level}\nhungar_level: {self.hungar_level}"


    def setSpecies(self, name):
        self.species = name


    def setAge(self, age):
        self.age = age


    def setHunger_level(self, hunger):
        self.hungar_level = hunger


    def changeThreat_level(self):
        self.threat_level = (["peacful"]*4 + ["narky"]*4 + ["aggressive"]*3)[self.hungar_level]
        return self.threat_level



cat = Animal(species="Cat", age=5)
cat.setSpecies("Cat")
cat.setAge(5)
cat.setHunger_level(7)
print(cat.changeThreat_level())
