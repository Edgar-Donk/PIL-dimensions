from dataclasses import dataclass, astuple
from PIL import ImageFont
'''
@dataclass
class Person:
    first_name: str = "Ahmed"
    last_name: str = "Besbes"
    age: int = 30
    job: str = "Data Scientist"

    #def __repr__(self):
        #return f"{self.first_name} {self.last_name} ({self.age})"

ahmed = Person()
print(astuple(ahmed))
# Ahmed Besbes (30)
'''
@dataclass(frozen=True)
class dc:
    image: str
    draw : str
    fill: tuple[int,int,int] = (0,0,0)
    back: tuple[int,int,int] = (255,255,221)
    arrow: str = 'both'
    arrowhead: tuple[int,int,int] = (8, 10, 3)
    font: str = ImageFont.truetype('consola.ttf', 12)
    aall: int = 1

    def __post_init__(self):
        if isinstance(arrowhead, tuple) and len(arrowhead) == 3:
            pass
        else:
            raise Exception('dataclass dc: arrowhead {} needs a 3 entry'  \
                'tuple'.format(arrowhead))

        if arrow not in ('first', 'last', 'both'):
            raise Exception('dimension_aa: arrow {} can only be the strings "first",' \
                '"last", "both"'.format(arrow))

        if isinstance(fill, tuple) and len(fill) == 3:
            pass
        else:
            raise Exception('dataclass dc: fill {} needs a 3 entry'  \
                'tuple'.format(fill))

        if isinstance(back, tuple) and len(back) == 3:
            pass
        else:
            raise Exception('dataclass dc: back {} needs a 3 entry'  \
                'tuple'.format(fill))

