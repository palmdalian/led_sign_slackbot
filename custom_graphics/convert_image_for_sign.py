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


image_string = ""

for line in image:
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
			image_string += "B"
		if R > 200 and G > 100:
			image_string += "Y"
		elif G > 200:
			image_string += "G"
			B = 0
		elif R > 200:
			image_string += "R"
		else:
			image_string += "B"
print(image_string)
print(1/ratio)

image = conform_colors(image)
big = cv2.resize(image, (0, 0), fx=1/ratio, fy=1/ratio, interpolation = cv2.INTER_NEAREST)
cv2.imshow('image',big)
cv2.waitKey(0)
cv2.destroyAllWindows()
