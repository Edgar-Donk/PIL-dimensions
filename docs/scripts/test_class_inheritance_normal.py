class Fish:
    def __init__(self, first_name, last_name="Fish",
                 skeleton="bone", eyelids=False):
        self.first_name = first_name
        self.last_name = last_name
        self.skeleton = skeleton
        self.eyelids = eyelids

    def swim(self):
        print("The fish is swimming.")

    def swim_backwards(self):
        print("The fish can swim backwards.")

class Pike(Fish):
    pass

class Clownfish(Fish):
    def live_with_anemone(self):
        print("The clownfish is coexisting with sea anemone.")

class Shark(Fish):
    def __init__(self, first_name, last_name="Shark",
                 skeleton="cartilage", eyelids=True):
        self.first_name = first_name
        self.last_name = last_name
        self.skeleton = skeleton
        self.eyelids = eyelids

    def swim_backwards(self):
        print("The shark cannot swim backwards, but can sink backwards.")

class Trout(Fish):
    def __init__(self, water = "freshwater"):
        self.water = water
        super().__init__(self)

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
terry = Trout()

# Initialize first name
terry.first_name = "Terry"

# Use parent __init__() through super()
print(terry.first_name + " " + terry.last_name)
print(terry.eyelids)

# Use child __init__() override
print(terry.water)

# Use parent swim() method
terry.swim()

'''
Percy Fish
bone
False
The fish is swimming.
The fish can swim backwards.

Casey Fish
The fish is swimming.
The clownfish is coexisting with sea anemone.

AttributeError: 'Pike' object has no attribute 'live_with_anemone'

Sammy Shark
The fish is swimming.
The shark cannot swim backwards, but can sink backwards.
True
cartilage

Terry Fish
False
freshwater
The fish is swimming.
'''