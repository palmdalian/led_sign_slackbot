import sys
import cv2

def conform_colors(img):
	for line_index, line in enumerate(img):
		for pixel_index, pixel in enumerate(line):
			B = pixel[0]
			G = pixel[1]
			R = pixel[2]
			if len(pixel) > 3:
				A = pixel[3]
				if (R > 200 and G > 200 and B > 200) or A < 100:
					# Turn white to black for now
					img[line_index][pixel_index] = [0, 0, 0, 255]
				elif R > 200 and G > 100:
					img[line_index][pixel_index] = [0, 255, 255, 255]
				elif G > 200:
					img[line_index][pixel_index] = [0, 255, 0, 255]
				elif R > 200:
					img[line_index][pixel_index] = [0, 0, 255, 255]
				else:
					img[line_index][pixel_index] = [0, 0, 0, 255]
			else:
				if (R > 200 and G > 200 and B > 200):
					# Turn white to black for now
					img[line_index][pixel_index] = [0, 0, 0]
				elif R > 200 and G > 100:
					img[line_index][pixel_index] = [0, 255, 255]
				elif G > 200:
					img[line_index][pixel_index] = [0, 255, 0]
				elif R > 200:
					img[line_index][pixel_index] = [0, 0, 255]
				else:
					img[line_index][pixel_index] = [0, 0, 0]
	return img

def pad_matrix(target_width, target_height, sign_matrix, fill_color):
	final_matrix = []
	if len(sign_matrix) < target_height:
		pad = target_height - len(sign_matrix)
		top_pad = int(pad/2)
		bottom_pad = int(pad/2)
		if pad % 2 != 0:
			top_pad += 1
		height_fill = []
		for i in xrange(0, target_width):
			height_fill.append(fill_color)
		
		for i in xrange(0, top_pad):
			sign_matrix.insert(0,height_fill)

		for i in xrange(0, bottom_pad):
			sign_matrix.append(height_fill)

	for line in sign_matrix:
		if len(line) < target_width:
			pad = target_width - len(line)
			left_pad = int(pad/2)
			right_pad = int(pad/2)
			if pad % 2 != 0:
				left_pad += 1

			for i in xrange(0, left_pad):
				line.insert(0, fill_color)
			for i in xrange(0, right_pad):
				line.append(fill_color)
	return sign_matrix


#IN BGR instead of RGB
image = cv2.imread (sys.argv[1], cv2.IMREAD_UNCHANGED)
height, width, channels = image.shape
target_width = 18
target_height = 7

if float(width / height) <= float(target_width / target_height):
	# Height is the restriction
	ratio = float(target_height) / float(height)
	print(ratio)
	image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)
else:
	# Width is the restriction
	ratio = float(target_width) / float(width)
	print(ratio)
	image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)

height, width, channels = image.shape
print("NEW height {} width {}".format(height, width))

xpad = 0
ypad = 0
sign_matrix = []

for line in image:
	sign_matrix.append([])
	for pixel in line:
		B = pixel[0]
		G = pixel[1]
		R = pixel[2]
		if len(pixel) > 3:
			A = pixel[3]
		else:
			A = 255
		if (R > 200 and G > 200 and B > 200) or A < 100:
			# Turn white to black for now
			sign_matrix[-1].append("B")
		if R > 200 and G > 100:
			sign_matrix[-1].append("Y")
		elif G > 200:
			sign_matrix[-1].append("G")
			B = 0
		elif R > 200:
			sign_matrix[-1].append("R")
		else:
			sign_matrix[-1].append("B")

final_matrix = pad_matrix(target_width, target_height, sign_matrix, "G")
image_string = ""
for row in final_matrix:
	image_string += "".join(row)

print image_string

image = conform_colors(image)
big = cv2.resize(image, (0, 0), fx=1/ratio, fy=1/ratio, interpolation = cv2.INTER_NEAREST)
cv2.imshow('image',big)
cv2.waitKey(0)
cv2.destroyAllWindows()
