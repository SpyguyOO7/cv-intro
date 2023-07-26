import cv2
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
#from dt_apriltags import Detector
import matplotlib.cm as cm

def detect_lines(img,threshold1 = 50,threshold2 = 150,apertureSize = 3,minLineLength=100,maxLineGap=10):
    """ takes an image as an input and returns a list of detected lines"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    blurred_image = cv2.GaussianBlur(gray, (9, 9), 0)
    edges = cv2.Canny(blurred_image, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
            edges,
            rho = 1,
            theta = np.pi/180,
            threshold = 100,
            minLineLength = minLineLength,
            maxLineGap = maxLineGap,

    )
    #print (lines)
    #be close enough, have similar slopes, be on the same side of the image
    return lines

def draw_lines(img,lines,color = (0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 6)
    return img

def get_slopes_intercepts(lines):
    resultSet = set() #stores the slope as the key, and the intercept as the data
    slopeList = []
    xInterceptList = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y1-y2)/(x1-x2)
        xIntercept = ((((1080 - y1)/slope)  )+ x1)
        roundXIntercept = round(xIntercept, 0)
        if not roundXIntercept in resultSet:
            resultSet.add(roundXIntercept) 
            xInterceptList.append(xIntercept)
        #    resultSet[slope][1] += 1 # keep a counter of how many lines have been iterated through and added to the one slope for averaging later
            slopeList.append(slope) 

    
    # for result in resultSet:
    #     #result[0] = result[0]/result[1] # apply the dividing in the averaging
    #     xInterceptList.append(result)

    return slopeList, xInterceptList

def detect_lanes(lines):
    slopeList, xInterceptList = get_slopes_intercepts(lines)
    #print (f"slopeList:{slopeList}")
    #print (f"xInterceptList:{xInterceptList}")
    lanes = []
    #check of the lines intersect on the screen
    if len(slopeList)> 1:
        for i in range(0,len(slopeList)):
            # if (len(slopeList) > 1):
            #     i += 1
            #     print("added i")
            for j in range (i+1,len(slopeList)):
                
                InterceptDist = abs(xInterceptList[i]-xInterceptList[j])
                slopeDiff = abs(1/ slopeList[i]-1 /slopeList[j]) 
                #print(f"DistREQ:{abs(xInterceptList[i]-xInterceptList[j])}")
                #print(f"slopeREQ:{abs(1/ slopeList[i]-1 /slopeList[j])}")
                if(InterceptDist > 100 and InterceptDist< 10000 and slopeDiff< 1):
                    
                    xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
                    yPoint = slopeList[i]*(xPoint - xInterceptList[i]) + 1080
                    
                    # avgSlope = (slopeList[i]+ slopeList[j])/2
                    # avgInterecept = (xInterceptList[i]+xInterceptList[j])/2
                    lane1 = [xInterceptList[i], 1080, xPoint, yPoint]
                    lane2 = [xInterceptList[j], 1080, xPoint, yPoint]
                    addedlanes = [lane1,lane2]
                    #print (f"thiasdfee:{(slopeList[i] * xInterceptList[i]) - slopeList[j] * xInterceptList[j]}")
                    lanes.append(addedlanes)


            #lanes.append(lane)

            #

            # if (yPoint> -500 and yPoint< 1080):
            #     avgInterceptX = (xInterceptList[i] + xInterceptList[j])/2
            #     lane = [xPoint.item(), avgInterceptX.item(), yPoint.item(), 1080.00]
            #     lanes.append(lane)

    return lanes

def pick_lane(lanes):
    maxDiff = 0
    for addedLanes in lanes:
        diff = abs(addedLanes[0][0]  - addedLanes[1][0])
        if (maxDiff < diff):
            maxDiff = diff
            pickedLane = addedLanes
    #print(f"picked: {pickedLane}")
    return pickedLane

def draw_lanes(img,lanes,color = (255, 0, 0)):
    for addedLanes in lanes:
        color = (randrange(255),randrange(255),randrange(255))
        for lane in addedLanes:
            
            x1, y1, x2, y2 = lane
       #     print ("type(x1)")
         #  print (lane)
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img

def draw_Single_lane(img,lanes,color = (255, 0, 0)):
    #color = (randrange(255),randrange(255),randrange(255))
    for lane in lanes:
        
        x1, y1, x2, y2 = lane
       # print ("type(x1)")
      #  print (lane)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img