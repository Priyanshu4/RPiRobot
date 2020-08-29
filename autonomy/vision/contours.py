import cv2

def getLargestContour(contours):
    largestArea = 0
    index = 0
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if(area > largestArea):
            largestArea = area
            index = i
    return contours[index]

def getMinX(contour):
    smallest = 1000000000
    index = 0
    for i in range(len(contour)):
        if(contour[i][0][0] < smallest):
            smallest = contour[i][0][0]
            index = i
    return smallest

def getMaxX(contour):
    largest = -1
    index = 0
    for i in range(len(contour)):
        if(contour[i][0][0] > largest):
            largest = contour[i][0][0]
            index = i
    return largest

def getMinY(contour):
    smallest = 1000000000
    index = 0
    for i in range(len(contour)):
        if(contour[i][0][1] < smallest):
            smallest = contour[i][0][1]
            index = i
    return smallest

def getMaxY(contour):
    largest = -1
    index = 0
    for i in range(len(contour)):
        if(contour[i][0][1] > largest):
            largest = contour[i][0][1]
            index = i
    return largest

