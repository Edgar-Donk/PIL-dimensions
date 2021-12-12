from PIL import Image, ImageDraw
from DimLinesAA import dimension_aa

if __name__ == '__main__':
    w, h = 640, 480
    im = Image.new('RGB', (w,h), '#FFFFDD')
    dr = ImageDraw.Draw(im)

    ptA = (110,110)
    ptB = (430,430)
    dimension_aa(im, dr, ptA, ptB, arrow='both', arrowhead=(8, 10, 3))
    ptA = (400,50)
    ptB = (50,400)
    dimension_aa(im, dr, ptA, ptB, arrow='both', arrowhead=(8, 10, 3))

    im.show()
    #im.save('../figures/test_dimension.png')