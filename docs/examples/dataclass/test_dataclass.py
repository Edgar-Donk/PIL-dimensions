from dataclasses import dataclass, field, fields
from PIL import ImageFont, Image, ImageDraw

def validate(instance):
    for field in fields(instance):
        attr = getattr(instance, field.name)
        print(attr, 'attr', field.name)
        #if not isinstance(attr, field.type) and field.name in (fill,back,arrowhead):
            #msg = "Field {0.name} is of type {1}, should be {0.type}".format(field, type(attr))
            #raise ValueError(msg)

@dataclass
class dc:
    width: int
    height: int
    image: str = field(init=False)
    draw : str = field(init=False)
    fill: tuple[int,int,int] = (0,0,0)
    back: tuple[int,int,int] = (255,255,221)
    arrow: str = 'both'
    arrowhead: tuple[int,int,int] = (8, 10, 3)
    tail: bool = True
    font: str = ImageFont.truetype('consola.ttf', 12)
    aall: int = 0

    def __post_init__(self):
        if self.arrow not in ('first', 'last', 'both'):
            raise Exception('dimension dc: arrow {} can only be the strings "first",' \
                '"last", "both"'.format(self.arrow))
        '''
        if isinstance(self.arrowhead, tuple) is False or len(self.arrowhead) != 3:
            raise Exception('dataclass dc: arrowhead {} needs a 3 entry'  \
                'tuple'.format(self.arrowhead))



        if isinstance(self.fill, tuple) is False or len(self.fill) != 3:
            raise Exception('dataclass dc: fill {} needs a 3 entry'  \
                'tuple'.format(self.fill))

        if isinstance(self.back, tuple) is False or len(self.back) != 3:
            raise Exception('dataclass dc: back {} needs a 3 entry'  \
                'tuple'.format(self.back))
        '''

        self.image = Image.new('RGB', (self.width, self.height), self.back)
        self.draw = ImageDraw.Draw(self.image)
        validate(self)

'''
arr='any'
im = Image.new('RGB', (300, 160), '#FFFFDD')
dr = ImageDraw.Draw(im)
#d = dc(im,dr,arrow=arr)
print(dc(im,dr))
print(dc.arrow)
'''
wi = 50
ht = 50
d = dc(wi,ht,arrow='first')
print('dc ',dc(wi,ht,arrow='first'))
#print('d ',d())

dc.arrow='last'
print(dc.arrow)
#d =
