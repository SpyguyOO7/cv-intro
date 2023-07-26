import cv2
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
    print (lines)
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
        slope = round(slope, 0)
        if not slope in resultSet:
            resultSet.add(slope) 
            xInterceptList.append(xIntercept)
        #    resultSet[slope][1] += 1 # keep a counter of how many lines have been iterated through and added to the one slope for averaging later
            slopeList.append(slope) 

    
    # for result in resultSet:
    #     #result[0] = result[0]/result[1] # apply the dividing in the averaging
    #     xInterceptList.append(result)

    return slopeList, xInterceptList

def detect_lanes(lines):
    slopeList, xInterceptList = get_slopes_intercepts(lines)
    print (f"slopeList:{slopeList}")
    print (f"xInterceptList:{xInterceptList}")
    lanes = []
    #check of the lines intersect on the screen
    for i in range(0,len(slopeList)):
        # if (len(slopeList) > 1):
        #     i += 1
        #     print("added i")
        for j in range (i,len(slopeList)):
            if(abs(xInterceptList[i]-xInterceptList[j])< 500):
                #print(f"xInterceptList:{xInterceptList[i]}")
                avgSlope = (slopeList[i]+ slopeList[j])/2
                avgInterecept = (xInterceptList[i]+xInterceptList[j])/2
                
                lane = [avgInterecept, 1080, (100)+avgInterecept,(avgSlope)* -100   +1080]
                print (f"lane:{lane}")
                lanes.append(lane)


            #lanes.append(lane)

            #xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
            #yPoint = slopeList[i]*(xPoint - xInterceptList[i])

            # if (yPoint> -500 and yPoint< 1080):
            #     avgInterceptX = (xInterceptList[i] + xInterceptList[j])/2
            #     lane = [xPoint.item(), avgInterceptX.item(), yPoint.item(), 1080.00]
            #     lanes.append(lane)

    return lanes

def draw_lanes(img,lanes,color = (255, 0, 0)):
    for lane in lanes:
        x1, y1, x2, y2 = lane
        print ("type(x1)")
        print (type(x1))
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img