from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append('../dims')

from DimLinesPIL import angled_text, dims
from numpy import linspace, concatenate, int_, astype

Font = ImageFont.truetype('consola.ttf', 12)

w, h = 100, 100
image = Image.new('RGB', (w,h), '#FFFFDD')

'''
both_arr =[(30, 10),
(30, 24),
(30, 40),
(30, 54),
(30, 70),
(30, 84)]
'''
start_arr = linspace((30, 10), (30, 70), 3)
end_arr = linspace((30, 24), (30, 84), 3)

both_arr = concatenate((start_arr, end_arr)) #, axis=0
#print(both_arr)

fin_arr = int_(both_arr[both_arr[:, 1].argsort()])
'''
 fin_arr [[30 10]
 [30 24]
 [30 40]
 [30 54]
 [30 70]
 [30 84]]
both_arr is different has comma between values
'''

print('len(fin_arr)', len(fin_arr), fin_arr)
nr_lines = len(fin_arr)

draw = ImageDraw.Draw(image)

[draw.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=1, fill='black')
            for n in range(0, nr_lines, 2)]

#width, height = Font.getsize(str(arr[4]))
unused1, unused2, width, height = Font.getbbox('(30, 84)') #Font.getbbox(str(arr[4]))

for i in range(nr_lines):
    angled_text(image, (fin_arr[i][0] + 10 + width//2, fin_arr[i][1]),text=str(fin_arr[i]),
            angle=0, fill='black', font=Font)

for j in range(nr_lines - 1):
    #TypeError: only length-1 arrays can be converted to Python scalars
    dims(image, draw, fin_arr[j], fin_arr[j+1], (8, 2), text='15', font=Font, fill='lightgreen',
        textorient='horizontal')
image.show()

