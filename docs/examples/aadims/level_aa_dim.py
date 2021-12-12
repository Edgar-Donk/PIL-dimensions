import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import sin, pi
from DimLinesAA import polyAA, DashedLineAA, LineAA
from DimLinesPIL import int_up, angled_text, DashedLine

def level_dim_aa(im, dr, at, diam, ext=0, ldrA=20, ldrB=20, dash=(10,4), text=None,
                fill=(0,0,0), back=(255,255,221), tri=8, font=None):
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

    if font is None:
        font = ImageFont.load_default()

    tsize = font.getsize(text) if text is not None else (0,0)

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

    if ldr_s < tsize[0]:
        raise Exception('The leader size is too small: {} should be larger '\
                        'than the text width {}'.format(ldr_s, tsize))

    p2 = (int_up(p0[0] + tri * 0.5), p0[1] - int_up(tri * sin(pi/3)))
    p1 = (p2[0] - tri, p2[1])
    p3 = (at[0] + diam, at[1]) # outer wall

    DashedLine(dr, at, end_pos=p3, dash=dash, width = 1, fill=fill)
    polyAA(im, dr, [p0, p1, p2], outline=(0,0,0))

    if ldrA > 0:
        if ext == 0:
            DashedLineAA(dr, p2, p4, dash=dash, fill=fill, back=back)
        else:
            LineAA(dr, p2, p4, fill=fill, back=back)
            dr.line([p3, (p3[0] + exto, at[1])], width = 1, fill=fill)
    else:
        if ext ==0:
            DashedLineAA(dr, p1, p4, dash=dash, fill=(255,0,0))
        else:
            LineAA(dr, p1, p4, fill=fill, back=back)
            dr.line([at, (at[0] - exto, at[1])], width = 1, fill=fill)

    if ext == 0:
        DashedLineAA(dr, p4, p5, dash=dash, fill=fill)
    else:
        dr.line([p4, p5], width = 1, fill=fill)

    p6 = (int((p4[0] + p5[0])//2), p4[1] - height - 5)

    angled_text(im, p6, text, angle, font, fill=fill)

if __name__ == "__main__":
    Text = '1250 hl'
    Font = ImageFont.truetype('consola.ttf', 12)
    wide, height = Font.getsize('(30, 84)')

    w, h = 200, 200
    image = Image.new('RGB', (w,h), '#FFFFDD')

    draw = ImageDraw.Draw(image)

    a = (90,10) #a=(10,10) # (50,10) #
    b = (90,190) # b=(10,190) # (50,380) #
    c = (110,10) # c=(190,10) # (110,10) #
    d = (110,190) # d=(190,190) # (110,380) #

    draw.line([a,b], width=2, fill=(0,0,255))
    draw.line([c,d], width=2, fill=(0,0,255))



    At=(a[0],100)
    Diam = c[0] - a[0]
    '''
    slant_dim_aa(image, draw, (144,164), extA=(10,4), length=40,
                angle=120, text='ldrA',font=font, fill=(0,0,255))

    slant_dim_aa(image, draw, (127,83), extA=(10,2), length=50,
                angle=0, text='extB',font=font)

    leader_aa(image, draw,(200,162),angle=315,extA=20,extB=30,text='ldrB',
                font=font, fill=(0,0,255))
    leader_aa(image, draw,(120,202),angle=45,extA=60,extB=30,text='ext',
                font=font, fill=(0,0,255))
    '''
    Fill=(0,0,0)

    level_dim_aa(image, draw, At, Diam, ext=(8,3), ldrA=-20, ldrB=50, dash=(5,5),
                fill=Fill, tri=8, font=Font, text=Text)

    image.show()
    #image.save('../../temp/out_level_dim_neg.png')