import attr
from PIL import ImageFont, Image, ImageDraw

def rgb_tuple(instance, attribute, var):
    if isinstance(var, tuple) is False or len(var) !=3:
        raise Exception('attr class atr: {} needs a 3 entry tuple'.format(var))

@attr.s(slots=True, auto_attribs=True)
class atr:
    width: int = attr.ib(init=False)
    height: int = attr.ib(init=False)
    image: str = attr.ib(init=False)
    draw : str = attr.ib(init=False)
    fill: tuple[int] = attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default=(0,0,0))
    back: tuple[int] = attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default=(255,255,221))
    #arrow: str = attr.ib(validator=attr.validators.in_(['first', 'last', 'both']),
            #default='both')
    arrowhead: tuple[int] =attr.ib(validator=[attr.validators.instance_of(tuple),
            rgb_tuple], default = (8,10,3))
    tail: bool = True
    font: str = ImageFont.truetype('consola.ttf', 12)
    aall: int = 0

    def __attrs_post_init__(self):
        self.image = Image.new('RGB', (self.width, self.height), self.back)
        self.draw = ImageDraw.Draw(self.image)

#im = Image.new('RGB', (100, 100), (255,255,221))

aq = atr()

# https://pymotw.com/2/socket/binary.html