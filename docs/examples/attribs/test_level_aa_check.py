import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw, ImageFont
from math import sin, pi
from DimLinesPIL import int_up, DashedLine, angled_text
from DimLinesattr import aq, WideLineATTR, DashedLineATTR, polyATTR, LineATTR


def level_dim_attr(at, diam, ext=(15, 3), ldrA=20, ldrB=50, dash=(10,4),
                text=None, tri=8):
    # at on left tank wall, diam internal tank diameter,
    # triangle at level (8,8,8) p0 tip triangle, p1, p2 angles, p2 continues to-p4
    # p3 opposite side to at, both drawn to inside tank wall
    # leader (ldr) at 60° up to p4 then horizontal to p5

    # check dash input
    if len(dash)%2 == 0 or len(dash) ==1:
        pass
    else:
        raise Exception('out_dim_level: the dash tuple {} should be one or an' \
                        ' equal number of entries'.format(dash))

    if isinstance(ext, int) or len(ext) == 1:
        exto = ext if isinstance(ext, int) else ext[0]
    elif len(ext) == 2:
        exto = sum(ext)
    else:
        raise Exception('out_dim_level: The extension tuple ext {} should be one' \
                        ' or two entries'.format(ext))

    # wide = aq.font.getsize(text) if text is not None else (0,0)
    wide = aq.font.getbbox(text) if text is not None else (0,0)

    angle = 0

    # check whether left or right position
    if ldrA > 0:
        if ext == 0:
            p0 = (int_up(at[0] + diam * 0.4), at[1])
            p4 = (int_up(p0[0] + ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3)))
            p5 = (at[0] + diam, p4[1]) if ldrB < diam else (at[0] + diam + ldrB, p4[1])
        else:
            p0 = (int_up(at[0] + diam + 0.6 * exto), at[1]) # tip triangle
            p4 = (int_up(p0[0] + ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3))) # top ldr
            p5 = (p4[0] + ldrB, p4[1]) # end ldr
    else:
        if ext == 0:
            p0 = (int_up(at[0] + diam * 0.6), at[1])
            p4 = (int_up(p0[0] + ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (at[0], p4[1])
        else:
            p0 = (int_up(at[0] - 0.6 * exto), at[1])
            p4 = (int_up(p0[0] + ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (p4[0] - ldrB, p4[1])

    ldr_s = abs(p5[0] - p4[0])

    if ldr_s < wide[2]:
        raise Exception('The leader size is too small: {} should be larger '\
                        'than the text width {}'.format(ldr_s, wide))

    p2 = (int_up(p0[0] + tri * 0.5), p0[1] - int_up(tri * sin(pi/3)))
    p1 = (p2[0] - tri, p2[1])
    p3 = (at[0] + diam, at[1]) # outer wall

    DashedLine(aq.draw, at, end_pos=p3, dash=dash, width = 1, fill=aq.fill)
    polyATTR([p0, p1, p2], outline=(0,0,0))
    if ldrA > 0:
        if ext == 0:
            DashedLineATTR(p2, p4, dash=dash)
        else:
            LineATTR(p2, p4)
            aq.draw.line([p3, (p3[0] + exto, at[1])], width = 1, fill=aq.fill)
    else:
        if ext ==0:
            DashedLineATTR(p1, p4, dash=dash)
        else:
            LineATTR(p1, p4, fill=aq.fill, back=aq.back)
            aq.draw.line([at, (at[0] - exto, at[1])], width = 1, fill=aq.fill)

    if ext == 0:
        DashedLineATTR(p4, p5, dash=dash)
    else:
        aq.draw.line([p4, p5], width = 1, fill=aq.fill)

    p6 = (int((p4[0] + p5[0])//2), p4[1] - wide[3] - 5)

    angled_text(aq.image, p6, text, angle, aq.font, fill=aq.fill)

    print(p0,p1,p2,p3,p4,p5,p6)

if __name__ == "__main__":

    Text='2500 hl'
    #font = ImageFont.truetype('consola.ttf', 12)
    #wide, height = aq.font.getsize(Text)

    #back = (255,255,221)

    #w, h = 200, 200
    #image = Image.new('RGB', (w,h), back)

    #draw = ImageDraw.Draw(image)

    a=(90,10)
    b=(90,190)
    c=(110,10)
    d=(110,190)
    fill = (0,0,255)

    WideLineATTR(a, b, width=2)
    WideLineATTR(c, d, width=2)

    At=(a[0],100)
    Diam = c[0] - a[0]



    level_dim_attr(At, Diam, ldrA=20, ldrB=50, dash=(10,4), text=Text,
                 tri=8)
    #level_dim_attr(im, dr, at, diam, ext=(15, 3), ldrA=20, ldrB=20, dash=(10,4), text=None,
                #fill=(0,0,0), tri=8, font=None)

    aq.image.show()
    #image.save('../../temp/level_dim_attr_pos.png')
