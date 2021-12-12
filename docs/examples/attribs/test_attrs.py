from PIL import ImageFont, Image, ImageDraw
import attr

def rgb_tuple(instance, attribute, var):
    if isinstance(var, tuple) is False or len(var) !=3:
        raise Exception('attr class atr: {} needs a 3 entry tuple'.format(var))

@attr.s(slots=True, auto_attribs=True)
class atr:
    width: int
    height: int
    image: str = attr.ib(init=False)
    draw : str = attr.ib(init=False)

    fill: tuple[int] = attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default=(0,0,0))
    back: tuple[int] = attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default=(255,255,221))
    arrow: str = attr.ib(validator=attr.validators.in_(['first', 'last', 'both']),
            default='both')
    arrowhead: tuple[int] =attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default = (8,10,3))
    tail: bool = True
    font: str = ImageFont.truetype('consola.ttf', 12)
    aall: int = 0

    def __attrs_post_init__(self):
        self.image = Image.new('RGB', (self.width, self.height), self.back)
        self.draw = ImageDraw.Draw(self.image)

@attr.s(slots=True, auto_attribs=True)
class arr:
    arrow: str = attr.ib(validator=attr.validators.in_(['first', 'last', 'both']),
            default='both')

#im = Image.new('RGB', (100, 100), (255,255,221))

'''
a = atr(100,100)
print(a.fill)
print(a,'first')

a = atr(100,100, fill=(255,0,0))
#a.fill=(255,0,0)

print(a, 'second')

#a.arrow='red'
a = atr(100,100, arrow='last')
print(a, 'third')
#a = atr(im, back=(255,0,0,0))
#a=atr()
#print(a, 'fourth')
print(atr.arrow, a.back,'atr.arrow, a.arrow')
'''
ar = arr()
print(ar)
ar = arr(arrow='first')
print(ar)