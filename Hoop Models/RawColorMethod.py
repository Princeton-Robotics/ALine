import cv2
import imutils
import numpy as np

image = cv2.imread('/Users/kyleaj/Desktop/IMG_0126.jpg', cv2.IMREAD_COLOR)
orange = np.array([24, 48, 172])
thresh = 20

im = imutils.resize(image, width=256)

width, height, channels = im.shape

# width, height = cv2.GetSize(image)

mask = np.zeros((width, height))

test = im[0, 0, :] - orange
print(im[0, 0, :])
print(orange)
print(test)

for w in range(width):
    for h in range(height):
        thisColor = im[w, h, :]
        thisColor = thisColor - orange
        thisColor = thisColor * thisColor
        dist = thisColor.sum()
        dist = np.sqrt(dist)
        #print(dist)
        if (dist <= thresh):
            mask[w, h] = 1

cv2.imshow('mask', mask)
cv2.imshow('orig', im)

cv2.waitKey(0)

cv2.destroyAllWindows()
