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

We can extend Fish class with a child class **Clownfish**.::

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

The answers should mostly differ from the Pike results::

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
variables are initiated that they are first created as an attribute, which may
or not have a default value, in which case they are pushed out of sequence 
to the end, then
in the body of the initialisation each attribute is attributed to a clone
of itself - the variable has been created in triplicate. Since Python 3.7 
there has been the builtin ability to simplify this using Dataclasses.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_normal.py

    .. literalinclude:: ../scripts/test_class_inheritance_normal.py


Dataclass
=========

Rebuild the classic classes as dataclasses. In particular see whether
inheritance is affected, if so how can it be improved. As above begin with
**Fish** class. This is rewritten, not forgetting the dataclass decorator::

    from dataclasses import dataclass

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

Initialisation for **Fish** falls away, but the two methods remain unaltered, 
with their reference to **self** (as before). The variables all come complete 
with their preferred type. The Pike class can be imported unchanged::

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

exactly as before. Add the Clownfish with its tests, also unchanged::

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

Test anemones with Pike::

    percy.live_with_anemone()

output as before::

    AttributeError: 'Pike' object has no attribute 'live_with_anemone'

Onto the shark which needs a decorator but can be simplified, much as before 
for fish::

    @dataclass
    class Shark(Fish):
        first_name:str
        last_name:str = "Shark"
        skeleton:str = "cartilage"
        eyelids:bool = True

    def swim_backwards(self):
        print("The shark cannot swim backwards, but can sink backwards.")

Many of the variables change, the swim method remains unaltered, (it is 
automatically included when we write **Shark(Fish)**), the other method was 
modifified in the new Shark class::

    sammy = Shark("Sammy")
    print(sammy.first_name + " " + sammy.last_name)
    sammy.swim()
    sammy.swim_backwards()
    print(sammy.eyelids)
    print(sammy.skeleton)

Lastly we come to the Trout class, which with its addition of water and
its **super** construct will need a dataclass decorator::

    @dataclass
    class Trout(Fish):
        water:str = "freshwater"

Run our tests as before::

    terry = Trout()
    
caused an error::

    TypeError: Trout.__init__() missing 1 required positional argument: 'first_name'

This means we cannot use terry.first_name = "Terry", try 
**terry = Trout("Terry")** ::

    # Initialize first name
    terry = Trout("Terry")

    # Use parent values for last name and eyelids
    print(terry.first_name + " " + terry.last_name)
    print(terry.eyelids)

    # Use new variable and its value
    print(terry.water)

    # Use parent swim() method
    terry.swim()
    
    # Use parent swim_backwards() method
    terry.swim_backwards()

The outcome is::

    Terry Fish
    False
    freshwater
    The fish is swimming.
    The fish can swim backwards. 

Apart from the slight hiccup when starting up the Trout class without a 
firstname all went well. It was lucky that our classes were rather simple.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_dc.py

    .. literalinclude:: ../scripts/test_class_inheritance_dc.py


Attrs
=====

The existing scripts used for the PIL dimensions had used the older version 
**attr**, this is accessible
with the newer version **attrs**, so until they are officially retired they 
can stay in use. The newer version is sleeker, so will be used for this 
exercise. Just as with the dataclass we only need to change those classes
which contain initialisation.

Apart from the imports and the attrs decorator **define** it is the same as
used for the dataclass, so type hints included. Copy all the dataclass
classes into a new file, change the imports and decorator, so when starting
the new **Fish** class will look like::

    from attrs import define

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
query with anemone at the end, to check that it can't be done.

Both methods (dataclass and attrs) work well, there are some advantages to 
both, but provided there is no restriction on using and installing third party
Python programs there seems to be an advantage with attrs.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_class_inheritance_attrs.py

    .. literalinclude:: ../scripts/test_class_inheritance_attrs.py

Applying dataclass and attrs
============================

Dataclasses and attrs work well where there is a lot of common data 
being changed and accessed. As seen above all valueless attributes (positional)
may need to be given values immediately when the class is first called, but 
this is similar to the behaviour of normal classes. Build a dataclass (attrs)
up from scratch rather than converting existing classes.

When converting classes, simple classes are better suited for dataclasses or 
attrs than those requiring unusual logic tucked away in a super class, normal 
inheritance rules can work, but as with everything test thoroughly. Classes 
with few if any values requiring to be initialised are not suited for 
dataclasses or attrs and the reasons to use them diminish if special 
constructions are required - whenever the class's methods are called the 
initial call is replaced by __post_init__ or the __attrs_post_init__ construct.