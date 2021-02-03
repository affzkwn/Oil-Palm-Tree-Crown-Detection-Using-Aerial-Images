import numpy as np
import cv2
import tkinter as tk
from matplotlib import pyplot as plt
from tkinter import filedialog
from PIL import Image, ImageCms


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

    # Open image and discard alpha channel which makes wheel round rather than square
im = Image.open(file_path ,"r").convert('RGB')

    # Convert to Lab colourspace
srgb_p = ImageCms.createProfile("sRGB")
lab_p  = ImageCms.createProfile("LAB")

rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, "RGB", "LAB")
Lab = ImageCms.applyTransform(im, rgb2lab)



    # Split into constituent channels so we can save 3 separate greyscales
L, a, b = Lab.split()

L.save('L.png')
a.save('a.png')
b.save('b.png')

img = cv2.imread('a.png',0)
blur = cv2.GaussianBlur(img, (5,5), 0)

rval, imgf = cv2.threshold(blur, 255, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

edges = cv2.Canny(imgf, 0,255)

cimg=cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,10,100,param1=255,param2=10,minRadius=20,maxRadius=30)

print (circles)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
       # draw the outer circle
       cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
       # draw the center of the circle
       cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
   
plt.imshow (cimg)
plt.title('detected crown'), plt.xticks([]), plt.yticks([])
print(circles.shape)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

