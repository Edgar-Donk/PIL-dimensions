from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append('../dims')

from DimLinesPIL import angled_text, dims
from numpy import linspace, concatenate, argsort, int_

Font = ImageFont.truetype('consola.ttf', 12)

w, h = 100, 100
image = Image.new('RGB', (w,h), '#FFFFDD')

'''
arr =[(30, 10),
(30, 24),
(30, 40),
(30, 54),
(30, 70),
(30, 84)]
'''
start_arr = linspace((30, 10), (30, 70), 3)
end_arr = linspace((30, 24), (30, 84), 3)

both_arr = concatenate([start_arr, end_arr], axis=0)

arr = int_(both_arr[both_arr[:, 1].argsort()])
'''
 arr [[30 10]
 [30 24]
 [30 40]
 [30 54]
 [30 70]
 [30 84]]
array is different needs comma between values
'''
print('len(arr)', len(arr), arr)
nr_lines = len(arr)

draw = ImageDraw.Draw(image)

[draw.line([tuple(arr[n]), tuple(arr[n+1])], width=1, fill='black')
            for n in range(0, nr_lines, 2)]

#width, height = Font.getsize(str(arr[4]))
unused1, unused2, width, height = Font.getbbox(str(arr[4]))

for i in range(nr_lines):
    angled_text(image, (arr[i][0] + 10 + width//2, arr[i][1]),text=str(arr[i]),
            angle=0, fill='black', font=Font)

for j in range(nr_lines - 1):
    #TypeError: only length-1 arrays can be converted to Python scalars
    dims(image, draw, arr[j], arr[j+1], (8, 2), text='15', font=Font, fill='lightgreen',
        textorient='horizontal')

image.show()

