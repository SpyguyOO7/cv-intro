import cv2
import numpy as np
import matplotlib.pyplot as plt
#from dt_apriltags import Detector
import matplotlib.cm as cm

def detect_lines(img,threshold1 = 50,threshold2 = 150,apertureSize = 3,minLineLength=100,maxLineGap=10):
    """ takes an image as an input and returns a list of detected lines"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi/180,
            100,
            minLineLength,
            maxLineGap,

    )
    return lines

def draw_lines(img,lines,color = (0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    return img

def get_slopes_intercepts(lines):
    resultSet = set() #stores the slope as the key, and the intercept as the data
    slopeList = []
    xInterceptList = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y1-y2)/(x1-x2)
        xIntercept = ((slope* x1) - y1)/slope
        slope = round(slope,1)
        if slope in resultSet:
            resultSet[slope][0] += xIntercept
            resultSet[slope][1] += 1 # keep a counter of how many lines have been iterated through and added to the one slope for averaging later
        else:
            resultSet.add([xIntercept,0])

    
    for result in resultSet:
        result[0] = result[0]/result[1] # apply the dividing in the averaging
        xInterceptList.append(result[0])

    return slopeList, xInterceptList

def detect_lanes(lines):

