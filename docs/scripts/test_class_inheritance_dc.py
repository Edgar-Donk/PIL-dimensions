from dataclasses import dataclass, field

@dataclass
class Fish:
    first_name:str
    last_name:str = "Fish"
    skeleton:str = "bone"
    eyelids:bool = False

    def swim(self):
        print("The fish is swimming.")

    def swim_backwards(self):
        print("The fish can swim backwards.")

class Pike(Fish):
    pass

class Clownfish(Fish):

    def live_with_anemone(self):
        print("The clownfish is coexisting with sea anemone.")

@dataclass
class Shark(Fish):
    first_name:str
    last_name:str = "Shark"
    skeleton:str = "cartilage"
    eyelids:bool = True

    def swim_backwards(self):
        print("The shark cannot swim backwards, but can sink backwards.")

@dataclass
class Trout(Fish):
    water:str = "freshwater"

percy = Pike("Percy")
print(percy.first_name + " " + percy.last_name)
print(percy.skeleton)
print(percy.eyelids)
percy.swim()
percy.swim_backwards()
print()

casey = Clownfish("Casey")
print(casey.first_name + " " + casey.last_name)
casey.swim()
casey.live_with_anemone()

print()

# percy.live_with_anemone()
print()

sammy = Shark("Sammy")
print(sammy.first_name + " " + sammy.last_name)
sammy.swim()
sammy.swim_backwards()
print(sammy.eyelids)
print(sammy.skeleton)

print()

#terry = Trout()

# Initialize first name
#terry.first_name = "Terry"

terry = Trout("Terry")

# Use parent __init__() through super()
print(terry.first_name + " " + terry.last_name)
print(terry.eyelids)

# Use child __init__() override
print(terry.water)

# Use parent swim() method
terry.swim()

terry.swim_backwards()
