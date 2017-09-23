import sys
import cv2

#IN BGR instead of RGB
image = cv2.imread (sys.argv[1])

image_string = ""

for line in image:
	for pixel in line:
		B = pixel[0]
		G = pixel[1]
		R = pixel[2]
		if R > 200 and G > 200 and B > 200:
			# Turn white to black for now
			image_string += "B"
		if R > 200 and G > 100:
			image_string += "Y"
		elif G > 200:
			image_string += "G"
		elif R > 200:
			image_string += "R"
		else:
			image_string += "B"
print(image_string)
