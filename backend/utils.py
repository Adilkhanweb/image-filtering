import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline

from scipy.interpolate import UnivariateSpline


def lookup_table(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))


def get_filtered_image(image, action):
    img = image
    filtered = None
    if action == 'no filter':
        filtered = image
    elif action == 'colorized':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif action == 'grayscale':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'blurred':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif 200 < width <= 500:
            k = (25, 25)
        else:
            k = (10, 10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'binary':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'invert':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    elif action == 'less bright':
        filtered = cv2.convertScaleAbs(img, beta=-60)
    elif action == 'more bright':
        filtered = cv2.convertScaleAbs(img, beta=60)
    elif action == 'sharpen':
        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        filtered = cv2.filter2D(img, -1, kernel)
    elif action == 'sepia':
        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        img_sepia = np.array(img, dtype=np.float64)  # converting to float to prevent loss
        img_sepia = cv2.transform(img_sepia, np.matrix(sepia_filter))  # multipying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = 255  # normalizing values greater than 255 to 255
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        filtered = img_sepia
    elif action == 'grey pencil sketch':
        # inbuilt function to create sketch effect in colour and greyscale
        filtered, sk_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    elif action == 'color pencil sketch':
        sk_gray, filtered = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    elif action == 'hdr':
        filtered = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    elif action == 'summer':
        increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel, red_channel = cv2.split(img)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        filtered = cv2.merge((blue_channel, green_channel, red_channel))
    elif action == 'winter':
        increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel, red_channel = cv2.split(img)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        filtered = cv2.merge((blue_channel, green_channel, red_channel))
    return filtered
