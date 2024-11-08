import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import sin, pi
from DimLinesAA import WideLineAA, DashedLineAA, polyAA
from DimLinesPIL import int_up, angled_text


def level_dim_aa(im, dr, at, diam, ext=(15, 3), ldrA=20, ldrB=50, dash=(10,4),
                text=None, fill=(0,0,0), back=(255,255,221), tri=8, font=None):
    # at on left tank wall, diam internal tank diameter,
    # triangle at level (8,8,8) p0 tip triangle, p1, p2 angles, p2 continues to p4
    # p3 opposite side to at, both drawn to inside tank wall
    # leader (ldr) at 60° up to p4 then horizontal to p5
    # if ext != 0, p7 position of end of extender before touching tank wall

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

    font = ImageFont.load_default() if font is None else font

    # (wide, ht) = font.getsize(text) if text is not None else (0,0)
    unused1, unused2, wide, ht = font.getbbox(text) if text is not None else (0,0)

    #hi = ht // 2

    angle = 0

    # check whether gap is required
    est = 0 if isinstance(ext, int) or len(ext) == 1 else ext[1] + 1
    print(exto)
    p3 = (at[0] + diam, at[1])
    # check whether left or right position
    if ldrA > 0:
        if ext == 0:
            p0 = (at[0] + int_up(diam * 0.4), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3)))
            p5 = (at[0] + diam, p4[1]) if ldrB < diam else (at[0] + diam + ldrB, p4[1])
        else:
            p0 = (at[0] + int_up(diam + 0.6 * exto), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3)))
            p5 = (p4[0] + ldrB, p4[1])  # end ldr
            p7 = (p3[0] + est, at[1])
    else:
        if ext == 0:
            p0 = (at[0] + int_up(diam * 0.6), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (at[0], p4[1])
        else:
            p0 = (at[0] - int_up(0.6 * exto), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (p4[0] - ldrB, p4[1])
            p7 = (at[0] - est, at[1])

    print(p4,p5)
    ldr_s = abs(p5[0] - p4[0])

    if ldr_s < wide:
        raise Exception('The leader size is too small: {} should be larger '\
                        'than the text width {}'.format(ldr_s, wide))

    p2 = (int_up(p0[0] + tri * 0.5), p0[1] - int_up(tri * sin(pi/3)))
    p1 = (p2[0] - tri, p2[1])

    DashedLineAA(dr, at, p3, dash=dash, fill=fill, back=back)
    polyAA(im, dr, [p0, p1, p2], outline=fill, back=back)

    if ldrA > 0:
        if ext == 0:
            DashedLineAA(dr, p2, p4, dash=dash, fill=fill, back=back)
        else:
            dr.line([p2, p4], width = 1, fill=fill)
            dr.line([p7, (p7[0] + exto, p7[1])], width = 1, fill=fill)
    else:
        if ext == 0:
            DashedLineAA(dr, p1, p4, dash=dash, fill=fill, back=back)
        else:
            dr.line([p1, p4], width = 1, fill=fill)
            dr.line([p7, (p7[0] - exto, p7[1])], width = 1, fill=fill)

    if ext == 0:
        DashedLineAA(dr, p4, p5, dash=dash, fill=fill, back=back)
    else:
        dr.line([p4, p5], width = 1, fill=fill)

    p6 = (int((p4[0] + p5[0])//2), p4[1] - ht - 5)

    angled_text(im, p6, text, angle, font, fill=fill)
    #print(p0,p1,p2,p3,p4,p5,p6) #,p7)

if __name__ == "__main__":

    Text='2500 hl'
    Font = ImageFont.truetype('consola.ttf', 12)
    # wi, height = Font.getsize(Text)
    unused1, unused2, wi, height = Font.getbbox(Text)

    Back = (255,255,221)

    w, h = 200, 200
    image = Image.new('RGB', (w,h), Back)

    draw = ImageDraw.Draw(image)

    a=(10,10) # (90,10)
    b=(10,190) # (90,190)
    c=(190,10) # (110,10)
    d=(190,190) # (110,190)
    Fill = (0,0,255)
    Fi = (0,0,0)

    WideLineAA(draw, a, b, width=2, fill=Fill, back=Back)
    WideLineAA(draw, c, d, width=2, fill=Fill, back=Back)

    At=(a[0],100)
    Diam = c[0] - a[0]

    #level_dim_aa(image, draw, At, Diam, ldrA=-20, ldrB=50, dash=(10,4), text=Text,
                #fill=Fi, back=Back, tri=8, font=Font)
    level_dim_aa(image, draw, At, Diam, ldrA=20, ldrB=50, dash=(10,4), text=Text,
                fill=Fi, back=Back, tri=8, font=Font, ext=0)

    image.show()
    #image.save('../../temp/out_level_aa_dim_neg.png')
