import cv2
import numpy as np


# function to detect objects in frame and draw contours, returns array
def detect_objects(frame):
    # convert to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect contours/edges
    mask = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # write contours to array
    objects_contours = []
    for each in contours:
        area = cv2.contourArea(each)
        if area > 2000:
            objects_contours.append(each)

    # return array of contours
    return objects_contours


# registering aruco dependencies
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

# read in image
img = cv2.imread("sample4_aruco.jpg")

# detect aruco square
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

# draw polygon around aruco square
int_corners = np.int0(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

# define scale of image
aruco_perimeter = cv2.arcLength(corners[0], True)
pixel_cm_ratio = aruco_perimeter / 20

# call detect_objects function
contours2 = detect_objects(img)

# draw object boundaries
for each in contours2:
    # create rectangle
    rect = cv2.minAreaRect(each)
    (x, y), (w, h), angle = rect

    # find dimensions in cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio

    # display rect
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # display center point and lines around rect
    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 2)

    # display width/height for testing purposes
    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN,
                2, (100, 200, 0), 2)
    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

# show results
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', 1080,1920)
cv2.imshow("Image", img)
cv2.waitKey(0)
