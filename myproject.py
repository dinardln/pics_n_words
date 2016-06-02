import os, sys
import string
from PIL import Image, ImageFilter

# Get path to image
ipath = input("Enter path to image: ")
if os.path.exists(ipath):
	ifile = os.path.basename(ipath)
	name, dot, ext = ifile.partition('.')
	if ext != "png":
		print("Invalid file extension")
		sys.exit()
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
	# img.show()
except:
	print("Unable to load image")


# write text file 
writer = open("output.txt", 'w')
with open(tpath) as open_file:
	for line in open_file:
		cl_line = line.strip()
		if cl_line:
			writer.write(cl_line)
writer.close()

with open("output.txt", 'r') as open_file:
	count = 0
	content = ""
	for line in open_file:
		count += len(line)
		content += line

# with open("output.txt")
print("Num chars: ", count)

print(content)

# find char array dims
x = 0
while (((x**2) * 144) < count):
	x += 1

print((x**2) * 144)
print(x)

index = 0
cols = 16 * x
rows = 9 * x
char_arr = [[' ' for c in range(cols)] for r in range(rows)]
# for i in range(rows):
# 	for j in range(cols):
# 		char_arr[i][j] = 

# print(char_arr[4][7])













