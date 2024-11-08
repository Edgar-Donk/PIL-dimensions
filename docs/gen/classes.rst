=======
Classes
=======

Classic Classes
===============

Classes as we all known are a powerful Python feature. `Digital Ocean <https://www.digitalocean.com/community/tutorials/understanding-class-inheritance-in-python-3>`_
has tutorials that explain how they work, in particular inheritance. Let's
demonstrate with the following based on Digital Ocean's knowhow.

Starting with a Class called **Fish** that has the basic attributes of the
family.::

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

The Fish class can be used directly, as in the class **Pike**.::

    class Pike(Fish):
        pass

This can be extended with a child class **Clownfish**.::

    class Clownfish(Fish):

        def live_with_anemone(self):
            print("The clownfish is coexisting with sea anemone.")

One can override the many of the variables in the parent class, as with 
**Shark** ::


    class Shark(Fish):
        def __init__(self, first_name, last_name="Shark", skeleton="cartilage", eyelids=True):
            self.first_name = first_name
            self.last_name = last_name
            self.skeleton = skeleton
            self.eyelids = eyelids
        def swim_backwards(self):
            print("The shark cannot swim backwards, but can sink backwards.")


If we need only to override a part of the parent class then the method using
super can be used as shown with the **Trout** class.::

    class Trout(Fish):
        def __init__(self, water = "freshwater"):
            self.water = water
            super().__init__(self)

These need to be tested and the output recorded. First test the Pike::

    percy = Pike("Percy")
    print(percy.first_name + " " + percy.last_name)
    print(percy.skeleton)
    print(percy.eyelids)
    percy.swim()
    percy.swim_backwards()

output::

    Percy Fish
    bone
    False
    The fish is swimming.
    The fish can swim backwards.

Now the Clownfish::

    casey = Clownfish("Casey")
    print(casey.first_name + " " + casey.last_name)
    casey.swim()
    casey.live_with_anemone()

its output::

    Casey Fish
    The fish is swimming.
    The clownfish is coexisting with sea anemone.

If we tried::

    percy.live_with_anemone()
    AttributeError: 'Pike' object has no attribute 'live_with_anemone'

Onto the Shark::

    sammy = Shark("Sammy")
    print(sammy.first_name + " " + sammy.last_name)
    sammy.swim()
    sammy.swim_backwards()
    print(sammy.eyelids)
    print(sammy.skeleton)

this should result mostly different from the Pike results::

    Sammy Shark
    The fish is swimming.
    The shark cannot swim backwards, but can sink backwards.
    True
    cartilage

Lastly the Trout::

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
    
    terry.swim_backwards()

giving the output::

    Terry Fish
    False
    freshwater
    The fish is swimming.
    The fish can swim backwards.

All should work as expected, but it should be pointed out that when 
variables are inititiated that they are first made as an attribute, which may
or not have a default value, in which case they are pushed to the end, then
in the body of the initialisation each attribute is attributed to a clone
of itself - they've been repeated twice over. Since Python 3.7 there has
been the builtin ability to simplify this using Dataclasses.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_normal.py

    .. literalinclude:: ../scripts/test_class_inheritance_normal.py


Dataclass
=========

Rebuild the classic classes as dataclasses. In particular see whether
inheritance is affected, if so how can it be improved. As above begin with
**Fish** class. This is rewritten, not forgetting the dataclass decorator::

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

Initialisation falls away, but the two methods remain unaltered, including
rererence to **self** (used for easier understanding). The variables all come
complete with their preferred type. The Pike class can be imported unchanged::

    class Pike(Fish):
        pass

let's see how it reacts::

    percy = Pike("Percy")
    print(percy.first_name + " " + percy.last_name)
    print(percy.skeleton)
    print(percy.eyelids)
    percy.swim()
    percy.swim_backwards()

output::

    Percy Fish
    bone
    False
    The fish is swimming.
    The fish can swim backwards.

exactly as before. Add the Clownfish and its tests, also unchanged::

    class Clownfish(Fish):

        def live_with_anemone(self):
            print("The clownfish is coexisting with sea anemone.")

Clownfish tests::

    casey = Clownfish("Casey")
    print(casey.first_name + " " + casey.last_name)
    casey.swim()
    casey.live_with_anemone()

once again correct::

    Casey Fish
    The fish is swimming.
    The clownfish is coexisting with sea anemone.

Test again with the Pike::

    percy.live_with_anemone()

output as before::

    AttributeError: 'Pike' object has no attribute 'live_with_anemone'

Onto the shark which needs attention, much as before for fish::

    @dataclass
    class Shark(Fish):
        first_name:str
        last_name:str = "Shark"
        skeleton:str = "cartilage"
        eyelids:bool = True

    def swim_backwards(self):
        print("The shark cannot swim backwards, but can sink backwards.")

Many of the variables change, one method remains unaltered the other was 
modified in the new Shark class::

    sammy = Shark("Sammy")
    print(sammy.first_name + " " + sammy.last_name)
    sammy.swim()
    sammy.swim_backwards()
    print(sammy.eyelids)
    print(sammy.skeleton)

Lastly we come to the Trout class, which with its duplication of water and
its **super** construct will need a dataclass decorator::

    @dataclass
    class Trout(Fish):
        water:str = "freshwater"

Run our tests as before::

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
    
    # Use parent swim_backwards() method
    terry.swim_backwards()

``terry = Trout()`` caused an error::

    TypeError: Trout.__init__() missing 1 required positional argument: 'first_name'

Try **terry = Trout("Terry")**

The outcome is::

    Terry Fish
    False
    freshwater
    The fish is swimming.
    The fish can swim backwards. 

Apart from the slight hiccup when starting up the Trout class without a 
firstname all went well. It was a bit of luck, but if it had not gone well
then we should have tried **key words** only.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_dc.py

    .. literalinclude:: ../scripts/test_class_inheritance_dc.py


Attrs
=====

The existing scripts had used the older version **attr**, this is accessible
with the newer version **attrs**, so until they are officially retired they 
can stay in use. The newer version is sleeker, so will be used for this 
exercise. Just as with the dataclass we only need to change those classes
with initialisation.

Apart from the imports and attrs decorator **define** it is the same as
used for the dataclass, also with types included. Copy all the dataclass
classes into a new file, change the imports and decorator, so when starting
the new **Fish** class will look like::

    from attrs import define, field

    @attrs
    class Fish:
        first_name:str
        last_name:str = "Fish"
        skeleton:str = "bone"
        eyelids:bool = False

        def swim(self):
            print("The fish is swimming.")

        def swim_backwards(self):
            print("The fish can swim backwards.")
            
    .....

and copy all the other classes, remembering the decorator changes for **shark**
and **trout**. Include all the queries as well as the original **Trout**
startup - just as with dataclass we had the slight hiccup. Place the Pike
query with anemone at the end, to check it can't be done.

Both methods (dataclass and attrs) work well, there are some advantages to 
both, but provided there is no restriction on using an installing third party
Python programs there seems to be an advantage with attrs.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_attrs.py

    .. literalinclude:: ../scripts/test_class_inheritance_attrs.py
