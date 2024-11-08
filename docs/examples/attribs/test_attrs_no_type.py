from PIL import ImageFont, Image, ImageDraw
import attr

def rgb_tuple(instance, attribute, var):
    if isinstance(var, tuple) is False or len(var) !=3:
        raise Exception('attr class atr: {} needs a 3 entry'  \
                'tuple'.format(var))

@attr.s(slots=True)
class atr:
    image = attr.ib()
    draw = attr.ib(init=False)

    #fill: tuple[int] = attr.ib(validator=[attr.validators.instance_of(tuple),
                        #default=(0,0,0))
    fill = attr.ib(default=(0,0,0))
    back = attr.ib(default=(255,255,221))
    arrow = attr.ib(validator=attr.validators.in_(['first', 'last', 'both']),
            default='both')
    #arrow: str = 'both'
    arrowhead = attr.ib(default=(8,10,3))
    tail = attr.ib(default=True)
    font = ImageFont.truetype('consola.ttf', 12)
    aall = attr.ib(default=0)

    def __attrs_post_init__(self):
        self.draw = ImageDraw.Draw(self.image)

        if isinstance(self.arrowhead, tuple) and len(self.arrowhead) == 3:
            pass
        else:
            raise Exception('attr class atr: arrowhead {} needs a 3 entry'  \
                'tuple'.format(self.arrowhead))

        if self.arrow not in ('first', 'last', 'both'):
            raise Exception('attr class atr: arrow {} can only be the strings "first",' \
                '"last", "both"'.format(self.arrow))

        if isinstance(self.fill, tuple) and len(self.fill) == 3:
            pass
        else:
            raise Exception('attr class atr: fill {} needs a 3 entry'  \
                'tuple'.format(self.fill))

        if isinstance(self.back, tuple) and len(self.back) == 3:
            pass
        else:
            raise Exception('atr class atr: back {} needs a 3 entry'  \
                'tuple'.format(self.back))

arr='any'
im = Image.new('RGB', (300, 160), (255,255,221))

a = atr(im, 'both')

print(a,'first')

# Exception: attr class atr: fill both needs a 3 entrytuple
a = atr(im, 'both', fill=(255,0,0))
#a.fill=(255,0,0)

print(a, 'second')

#a.arrow='red'
a = atr(im, 'red')
print(a, 'third')