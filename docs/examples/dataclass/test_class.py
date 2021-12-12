from PIL import ImageFont, Image, ImageDraw

class A:
    image: str
    draw : str
    fill: tuple[int,int,int] = (0,0,0)
    back: tuple[int,int,int] = (255,255,221)
    arrow: str = 'both'
    arrowhead: tuple[int,int,int] = (8, 10, 3)
    tail: bool = True
    font: str = ImageFont.truetype('consola.ttf', 12)
    aall: int = 0

print(A(), A.arrowhead)