import os, sys
import string
from PIL import Image, ImageFilter, ImageDraw, ImageFont

class pixel:
	r, g, b = 0, 0, 0

# Get path to image
ipath = input("Enter path to image: ")
if os.path.exists(ipath):
	ifile = os.path.basename(ipath)
	name, dot, ext = ifile.partition('.')
	# if ext != "png":
	# 	print("Invalid file extension")
	# 	sys.exit()
else:
	print("Path does not exist")
	sys.exit()

# Get path to text
tpath = input("Enter path to text file: ")
if os.path.exists(tpath):
	tfile = os.path.basename(tpath)
	name, dot, ext = tfile.partition('.')
	if ext != "txt":
		print("invalid file extension")
		sys.exit()

try:
	img = Image.open(ipath)
	print("Image properties: ", img.format, img.size, img.mode)
except:
	print("Unable to load image")

# Write text file to a string
try:
	with open(tpath, 'r') as open_file:
		count = 0 
		content = "" 
		for line in open_file:
			cl_line = line.strip()
			if cl_line:
				count += len(cl_line)
				content += cl_line
except:
	print("Unable to load text file")

print("Chars: ", count)

# find char array dimensions
# 144 = 19 * 6
dims = 0
while (((dims**2) * 144) < count):
	dims += 1

print("Dims: ", dims)

# Put string into 2d array of same size as original image
index = 0
cols = 16 * dims
rows = 9 * dims
xpx = 1920 / cols # 20
ypx = 1080 / rows # 20 

cur_r, cur_c = 0, 0 # 0 < r < rows

rgb_img = img.convert("RGB")

colors = [] # holds avg pixel color for each char

print("=== Processing Picture ===")

# find and save average pixel color for a region of the image
for r in range(int(round(rows))):
	for c in range(int(round(cols))): 
		x = cur_c * xpx
		y = cur_r * ypx
		tot_r, tot_g, tot_b = 0, 0, 0
		for y in range(int(round(cur_r * ypx)), int(round((cur_r * ypx) + ypx))):
			for x in range(int(round(cur_c * xpx)), int(round((cur_c * xpx) + xpx))):
				r, g, b = rgb_img.getpixel((x, y))
				tot_r += r
				tot_g += g
				tot_b += b
		cur_px = pixel()
		cur_px.r = int(round(tot_r / (xpx * ypx)))	
		cur_px.g = int(round(tot_g / (xpx * ypx)))
		cur_px.b = int(round(tot_b / (xpx * ypx)))
		colors.append(cur_px)
		cur_c += 1
	cur_r += 1
	cur_c = 0

print("=== Picture Processed ===")

char_arr = [[' ' for c in range(cols)] for r in range(rows)]
for i in range(rows):
	for j in range(cols):
		if index < count:
			char_arr[i][j] = content[index]
			index += 1

canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype("COURIER.ttf", 15) # font size is dependent on what x is

print("=== Creating Image ===")

index = 0
x, y = 0, 0
for i in range(rows):
	for j in range(cols):
		draw.text((x*10, y*12), char_arr[i][j], (colors[index].r, colors[index].g, colors[index].b), font = font) # spacing is dependent on what x is
		x += 1
		index += 1
	draw.text((0, 0), "\n", (0, 0, 0), font = font)
	x = 0
	y += 1

canvas.save("canvas.png", "PNG")

print("=== Image Saved ===")















