# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# PICS 'N' WORDS															  #
# Written by: Matt Peretick													  #
# Contact: mattjp@umich.edu													  #
#																			  #
# Takes a 1920 x 1080 image and text file paths as inputs. The program then   #
# reformats the text file as a rectangle with side length ratio of 16:9, with #
# input text having the same colors as the picture input. It outputs a .png   #
# file of the newly formatted and colored text. 							  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os, sys
import string
import random
from PIL import Image, ImageFilter, ImageDraw, ImageFont

def random_colors(colors) :

	my_color_dic = {}

	for color in colors :
		my_str = str(color.r) + str(color.g) + str(color.b)
		try :
			my_color_dic[my_str].append(color)
		except KeyError:
			my_color_dic[my_str] = []
			my_color_dic[my_str].append(color)

	new_colors = []

	for my_str_clr in my_color_dic :
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		print(r, g, b)
		for my_color in my_color_dic[my_str] :
			my_color.r = r
			my_color.g = g
			my_color.b = b
			new_colors.append(my_color)

	for color in colors :
		my_str = str(color.r) + str(color.g) + str(color.b)
		try:
			color = my_color_dic[my_str][0]
		except KeyError:
			continue

	
	return colors

# Class to save average cell color
class pixel:
	r, g, b = 0, 0, 0

# Get and validate path to image
ipath = input("Enter path to (1920x1080) image: ")
if os.path.exists(ipath):
	ifile = os.path.basename(ipath)
	name, dot, ext = ifile.partition('.')
	try:
		img = Image.open(ipath)
		print("Image properties: ", img.format, img.size, img.mode)
		if img.size != (1920, 1080):
			print("Incorrect image dimensions")
			sys.exit()
	except:
		print("Unable to load image")
		sys.exit()
else:
	print("Path does not exist")
	sys.exit()

# Get and validate path to text
tpath = input("Enter path to text file: ")
if os.path.exists(tpath):
	tfile = os.path.basename(tpath)
	name, dot, ext = tfile.partition('.')
	if ext != "txt":
		print("invalid file extension")
		sys.exit()

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
print("Character count: ", count)

# Find char array dimensions
dims = 0
while (((dims * 16) * (dims * 9)) < count):
	dims += 1
print("Dims: ", dims)

# Font size and spacing based on length of text file
font_size, x_spc, y_spc = 0, 0, 0
if dims == 1:
	font_size = 120
	x_spc = 120
	y_spc = 120
elif dims == 2:
	font_size = 80 
	x_spc = 60
	y_spc = 62
elif dims == 3:
	font_size = 60
	x_spc = 40
	y_spc = 39.5
elif dims == 4:
	font_size = 45
	x_spc = 30
	y_spc = 30
elif dims == 5:
	font_size = 40
	x_spc = 24
	y_spc = 23.5
elif dims == 6:
	font_size = 32
	x_spc = 20
	y_spc = 19.5
elif dims == 7:
	font_size = 24
	x_spc = 17.15
	y_spc = 17
elif dims == 8:
	font_size = 22
	x_spc = 15
	y_spc = 15
elif dims == 9:
	font_size = 20
	x_spc = 13.35
	y_spc = 13.3
elif dims == 10:
	font_size = 18
	x_spc = 12
	y_spc = 12
else:
	print("File contains too many characters")
	sys.exit()

# Each cell contains 1 char
cols = 16 * dims
rows = 9 * dims

# Cell size in pixels to determine char color
xpx = 1920 / cols 
ypx = 1080 / rows 

# List to hold char colors 
colors = [] 

# Find and save avg pixel color for each cell in the image
print("=== Processing Picture ===")
rgb_img = img.convert("RGB")
cur_r, cur_c = 0, 0 
for r in range(int(round(rows))):
	for c in range(int(round(cols))): 
		x = cur_c * xpx
		y = cur_r * ypx
		tot_r, tot_g, tot_b = 0, 0, 0
		for y in range(int(round(cur_r * ypx)), 
			int(round((cur_r * ypx) + ypx))):
			for x in range(int(round(cur_c * xpx)), 
				int(round((cur_c * xpx) + xpx))):
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

# Init 2D list. Each entry is 1 char of the text file
index = 0
char_arr = [[' ' for c in range(cols)] for r in range(rows)]
for i in range(rows):
	for j in range(cols):
		if index < count:
			char_arr[i][j] = content[index]
			index += 1

# Create new image with transparent background 
canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype("COURIER.ttf", font_size) 
colors = random_colors(colors)

# Print each char of the text file with the color of the cell avg
print("=== Creating Image ===")
index = 0
x, y = 0, 0
for i in range(rows):
	for j in range(cols):
		draw.text((x * x_spc, y * y_spc), char_arr[i][j], (colors[index].r, 
		colors[index].g, colors[index].b), font = font)
		x += 1
		index += 1
	draw.text((0, 0), "\n", (0, 0, 0), font = font)
	x = 0
	y += 1

# Save the image as "canvas.png"
canvas.save("canvas.png", "PNG")
print("=== Image Saved ===")



	
