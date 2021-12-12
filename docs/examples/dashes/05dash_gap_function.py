import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import dist
from numpy import linspace, concatenate, argsort, int_
from DimLinesPIL import angled_text, dims, int_up

def line_dashed(dr, start_pos, end_pos, dash=(5,5), width = 1, fill='black'):
    # create dashed lines in PIL

    # unpack tuples
    x0, y0 = start_pos
    x1, y1 = end_pos
    dash0, dash1 = dash
    dash2 = dash0 - 1

    # sort out lengths
    dash_gap_length = sum(dash)
    line_length = dist(start_pos, end_pos)

    # inclusive number of dashes and gaps
    dash_amount = int_up(line_length / dash_gap_length) + 1


    start_arr = linspace((x0, y0), (x1, y1), dash_amount)
    end_arr = linspace((x0, y0 + dash2), (x1, y1 + dash2), dash_amount)

    both_arr = concatenate([start_arr, end_arr], axis=0)

    fin_arr = int_(both_arr[both_arr[:, 1].argsort()])

    nr_lines = len(fin_arr)

    [dr.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=width, fill=fill)
            for n in range(0, nr_lines, 2)]

if __name__ == "__main__":
    Font = ImageFont.truetype('consola.ttf', 12)

    arr =[(30, 10),
    (30, 24),
    (30, 40),
    (30, 54),
    (30, 70),
    (30, 84)]

    nr_lines = len(arr)

    Dash =(15, 15)

    Start_pos = (30, 10)
    End_pos = (30, 70)

    w, h = 100, 100
    image = Image.new('RGB', (w,h), '#FFFFDD')
    draw = ImageDraw.Draw(image)

    wide, height = Font.getsize('(30, 84)')

    for i in range(nr_lines):
        angled_text(image, (arr[i][0] + 10 + wide//2, arr[i][1]),text=str(arr[i]),
                angle=0, fill='black', font=Font)

    for j in range(nr_lines - 1):
        dims(image, draw, arr[j], arr[j+1], (8, 2), text='15', font=Font, fill='lightgreen',
                textorient='horizontal')


    line_dashed(draw, Start_pos, End_pos, dash=Dash, width = 1, fill='black')

    image.show()
