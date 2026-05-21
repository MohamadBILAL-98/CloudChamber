import cv2
import sys
sys.path.insert(1, "../")
from cloudChamberCommonCode import rawDataDirectory, rawDataFileName

# open one image to see its content
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# load one corrected image
imageNumber = 100  # change this number to see different images
fileName = rawDataDirectory + "aber_" + rawDataFileName + str(imageNumber) + ".jpeg"
print("Opening:", fileName)

img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
print("Image shape:", img.shape)  # shows (height, width)

plt.figure(figsize=(12, 8))
plt.imshow(img, cmap='gray')
plt.colorbar()
plt.title("Image %d — click to find coordinates" % imageNumber)

# this shows coordinates when you move mouse over the image
plt.show()