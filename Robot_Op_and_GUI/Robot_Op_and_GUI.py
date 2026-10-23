###########################################Libraries######################################################################################

from operator import ge
from statistics import mean
import cv2 
import numpy as np
import pandas as pd
import math
import urllib
import os
import datetime
import time
import sys
import requests
import argparse
from urllib.request import urlopen
import math
import socket
import threading
import sys
import time
import os
from tkinter import *
from robot_library import *
import os
import sys
from tensorflow.keras.models import model_from_json

###########################################End of Libraries###############################################################################

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
mlp = model_from_json(loaded_model_json)
# load weights into new model
mlp.load_weights("model.h5")

###########################################Tkinter Buttons and Sliders####################################################################

master = Tk()

rack = -370 
tube = -440
# base = -445 
rack2 = -430 
list_height ={"rack":rack,"tube":tube,"rack2":rack2} #"base":base,
options = StringVar(master)
options.set(list_height["rack"]) # default value

l1 = Label(master,  text='Select Final Height')  
l1.grid(row=2,column=1) 

om1 = OptionMenu(master, options, *list_height)
om1.grid(row=2,column=2)

b1 = Button(master,  text='Click to Choose', command=lambda: my_show() )  
b1.grid(row=2,column=3)

str_out = StringVar(master)
str_out.set("Output")

l2 = Label(master,  textvariable=str_out, width=10 )  
l2.grid(row=2,column=4)

def my_show():
    global str_out,options,list_height
    # print(type(list_height))
    str_out.set(options.get())
    z_injection = list_height[options.get()]
    print(z_injection)


w1 = Scale(master, from_=0, to=100, tickinterval=10, length=600, orient=HORIZONTAL, label= "r_tube>")
w1.set(13)
w1.grid(row=3,columnspan =5)
w2 = Scale(master, from_=0, to=100, tickinterval=10, length=600, orient=HORIZONTAL, label= "r_tube<")
w2.set(40)
w2.grid(row=4,columnspan =5)
w3 = Scale(master, from_=35, to=65, tickinterval=5, length=600, orient=HORIZONTAL, label= "Tube_threshold")
w3.set(50)
w3.grid(row=5,columnspan =5)
w4 = Scale(master, from_=0, to=2, tickinterval=1, length=600, orient=HORIZONTAL, label= "Tube_threshold_method")
w4.set(1)
w4.grid(row=6,columnspan =5)
w5 = Scale(master, from_=0, to=2, tickinterval=1, length=600, orient=HORIZONTAL, label= "Rack_threshold_method")
w5.set(0)
w5.grid(row=7,columnspan =5)

i = 0
go_to_en = False
def go_to_en_func():
    # go_to_en = True
    global Delta , last_selected_coord,list_height,options
    if Delta:
        # cv2.imwrite("test.png",image_shapes_included)
        # print('Count: {}'.format(count))
        # print('\n',cordinate)
        # print(last_selected_coord)
        for row in np.array(last_selected_coord):
            [xx,yy,rr,con] = row
            transform_mat = np.array([[ 0.2410943 ,  0.        ],[ 0.        , -0.24016275]])
            input_mat = np.array([[xx],[yy]])
            [[x_pred],[y_pred]] = np.dot(transform_mat,input_mat)
            mean_x_tr = -194.20
            mean_y_tr = 123.31
            pred_x = x_pred + mean_x_tr
            pred_y = y_pred + mean_y_tr
            # input_temp = [xx,yy, 46.,  176.,   96.]
            # [[pred_x,pred_y]] = mlp.predict(([input_temp]))
            z_injection = int(list_height[options.get()])
            # print(f'camera {xx:.2f}\t{yy:.2f}\t{rr:.2f}')
            go_to(pred_x,pred_y,z_injection)
        # go_to_en = False
            
        move_to(0,0,-300)
        # for row in cordinate_sorted:
        #     go_to(row[0],row[1])
        #     #print(row[0],row[1])
        #     print(get_position(),"\n\n\n")
        # move_to(0,0,-300)


    
#Button(master, text='Show', command=show_values).pack()
# Button(master, text='rack', command=index(0)).pack()
# Button(master, text='tube', command=index(1)).pack()
# Button(master, text='base', command=index(2)).pack()
# Button(master, text='rack2', command=index(3)).pack()
Button(master, text='click to go', command=go_to_en_func).grid(row=8,columnspan =5)

###########################################END of Tkinter Buttons and Sliders#############################################################
###########################################robot capture##################################################################################

robot_capture = int(input("capture needed? \n 0: No\n 1: Yes\n")) 

if robot_capture == 1:
    Delta = capture()
    # print(get_position())
    time.sleep(5)
elif robot_capture == 0:
    Delta= True

###########################################END of robot capture###########################################################################
###########################################Global Variables###############################################################################

# newcam_mtx = np.load(os.path.join(os.getcwd(),"newcam_mtx.npy"))
# dist = np.load(os.path.join(os.getcwd(),"dist.npy"))
newcam_mtx = np.load(r".\newcam_mtx.npy")
dist = np.load(r".\dist.npy")
rack = -370 
tube = -330
base = -445 
rack2 = -400 
# list_height =[rack,tube,base,rack2]
#index = int(input("rack = 0\n tube = 1\n base = 2\n rack2 = 3\n choose height:"))
x_rack = 180
y_rack = 97
z_rack = 45
H = 430

font = cv2.FONT_HERSHEY_COMPLEX
ip="192.168.0.150 port:810 TCP "
#end effector cordinate

# url = r"C:\Users\TavanResan\Desktop\output\basicvideo.mp4"
#xga(1024*768
C=4 #Constant multiplier cm to show better result
#upper left cordinates in cm
x_upper_left=-194.20
y_upper_left=123.31
#y_upper_left=-6
#width = int(C*417*(38/44)) #mm
#height = int(C*254*(38/44)) #mm
width = C*407 #mm
height = C*256 #mm
#image = cv2.VideoCapture(0)
#image = cv2.VideoCapture(url)
region_of_interest_image = np.zeros([600,400])
imagedetected = np.full((width,height,3), 12, np.uint8)
Threshold_tube = np.full((width,height,3), 12, np.uint8)
# url = "basicvideo2.mp4"  change it************************************************
url = "http://192.168.4.1:81/stream"
image = cv2.VideoCapture(url)
#end effector cordinate
x0=-21.91
y0=-325.15
z0=-284.21
#preset values for 4 corners
x1=0
y1=0

x2=1023
y2=0

x3=1023
y3=767

x4=0
y4=76

###########################################End of Global Variables########################################################################



def compare_arrays(array1, array2, tolerance):
    output = []
    for row1 in array1:
        match_found = False
        for row2 in array2:
            if np.allclose(row1[:3], row2[:3], atol=tolerance):
                output.append(np.concatenate([row1[:3], [row2[3]]]))
                match_found = True
                break
        if not match_found:
            output.append(row1)
    for row2 in array2:
        match_found = False
        for row1 in array1:
            if np.allclose(row2[:3], row1[:3], atol=tolerance):
                match_found = True
                break
        if not match_found:
            output.append(row2)
    return np.array(output)

first_time = True

def doing_work(region_of_interest_image,img,event, x_mouse, y_mouse,count,xycoord,count_selected,last_count_selected,selected_coord,contours):
    if contours is not None:    
        # Code to draw rectangles around the detected tubes
        for contour in contours:
            ((x, y), r) = cv2.minEnclosingCircle(contour)
            # np.append(xycoord,coooooord)
            if r>13 and r<40 :
                if event == cv2.EVENT_LBUTTONDOWN and x-r<x_mouse<x+r and y-r<y_mouse<y+r:
                    coooooord = np.array([[x,y,r,1]])
                    # print('clicked') 
                    count_selected += 1
                    if count_selected ==1:
                        selected_coord = coooooord
                        # return xycoord
                    elif count_selected >1:
                        selected_coord = np.append(selected_coord,coooooord, axis=0)
                        # return xycoord
                    # print(x_mouse, ' ', y_mouse)
                else:
                    coooooord = np.array([[x,y,r,0]])
                    count += 1
                    if count ==1:
                        xycoord = coooooord
                        # return xycoord
                    elif count >1:
                        xycoord = np.append(xycoord,coooooord, axis=0)
                        # return xycoord            
            else :
                pass
        for en,row in enumerate(selected_coord):
            x = row[0]
            y = row[1]
            r = row[2]
            if event==cv2.EVENT_RBUTTONDOWN and x-r<x_mouse<x+r and y-r<y_mouse<y+r and r>13 and r<40:
                # print('clicked')
                coooooord = np.array([[x,y,r,2]])
                count_selected -= 1
                # print("found cleaning")
                cv2.circle(img,(int(x), int(y)), int(r),  (0, 0, 0), -1)
                selected_coord = np.delete(selected_coord,en,0)
                # row[3] = 0
                # if count_selected ==1:
                #     selected_coord = coooooord
                #     # return xycoord
                # elif count_selected >1:
                #     selected_coord = np.append(selected_coord,coooooord, axis=0)
                #     # return xycoord
        xycoord = np.array(xycoord)
        selected_coord = np.array(selected_coord)
        new_xycoord = compare_arrays(xycoord,selected_coord, tolerance=5)
        # print(f'xycoord={xycoord}')
        # print(f'count={count}')
        last_selected_coord = []
        for row in new_xycoord:
            # print(f'row={row}')
            x = row[0]
            y = row[1]
            r = row[2]
            if row[3] == 0:    
                if r>13 and r<40 and not (x-r<x_mouse<x+r and y-r<y_mouse<y+r):
                    cv2.circle(img,(int(row[0]), int(row[1])), int(row[2]), (36, 255, 12), -1)
                elif r>13 and r<40 and x-r<x_mouse<x+r and y-r<y_mouse<y+r:
                    cv2.circle(img,(int(row[0]), int(row[1])), int(row[2]+5), (36, 255, 12), -1)
            elif row[3] == 2 : #and x-r<x_mouse<x+r and y-r<y_mouse<y+r and r<50
                # print("found cleaning")
                cv2.circle(img,(int(row[0]), int(row[1])), int(row[2]),  (0, 0, 0), -1)
                row[3] = 0
                last_selected_coord.append(row)
            elif row[3] == 1 : #and x-r<x_mouse<x+r and y-r<y_mouse<y+r and r<50
                # print("found")
                # print(xycoord)
                cv2.circle(img,(int(row[0]), int(row[1])), int(row[2]), (255, 255, 0), -1)
                transform_mat = np.array([[ 0.2410943 ,  0.        ],[ 0.        , -0.24016275]])
                input_mat = np.array([[x],[y]])
                [[x_pred],[y_pred]] = np.dot(transform_mat,input_mat)
                mean_x_tr = -194.20
                mean_y_tr = 123.31
                x_pred = x_pred + mean_x_tr
                y_pred = y_pred + mean_y_tr
                cv2.putText(img, f"X={int(x_pred)}", (int(x-r), int(y-r/2)), cv2.QT_FONT_NORMAL, 0.4, (0, 0, 0), 1) ## comment xcm instead of x
                cv2.putText(img, f"Y={int(y_pred)}", (int(x-r), int(y)), cv2.QT_FONT_NORMAL, 0.4, (0, 0, 0), 1)
                cv2.putText(img, f"C={int(count)}", (int(x-r), int(y+r/2)), cv2.QT_FONT_NORMAL, 0.4, (0, 0, 0), 1)
                last_selected_coord.append(row)
        # last_selected_coord = np.copy(selected_coord)
        last_count_selected = count_selected
        cv2.imshow("Detected Tubes", img) 
        return last_selected_coord ,img ,  last_count_selected


def click_event(event, x_mouse, y_mouse, flags, params):
    global first_time
    (showing_image , region_of_interest_image) = params
    # gray = cv2.cvtColor(region_of_interest_image, cv2.COLOR_BGR2GRAY)
    gray = region_of_interest_image.copy()
    ret, thresh = cv2.threshold(gray, 180, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.circle(showing_image,(int(x_mouse), int(y_mouse)), int(2), (0, 255, 0), -1)
    # cv2.imshow("thresh", thresh)
    # cv2.imshow("Detected Tubes", img)
    count = 0
    xycoord = []
    if first_time:
        global last_count_selected , last_selected_coord
        count_selected = 0
        last_count_selected = 0
        selected_coord = []
        first_time = False
        last_selected_coord ,showing_image, last_count_selected = doing_work(region_of_interest_image,showing_image,event, x_mouse, y_mouse,count,xycoord,count_selected,last_count_selected,selected_coord,contours)
        # cv2.imshow("Detected Tubes", img) 
        return last_count_selected , last_selected_coord
    else:
        count_selected = last_count_selected
        selected_coord = np.copy(last_selected_coord)
        last_selected_coord ,showing_image, last_count_selected = doing_work(region_of_interest_image,showing_image,event, x_mouse, y_mouse,count,xycoord,count_selected,last_count_selected,selected_coord,contours)
        # cv2.imshow("Detected Tubes", img) 
        




###########################################Camera Calibration#############################################################################

def camera_calibration(image):
    global newcam_mtx,dist
    map1 , map2 = cv2.initUndistortRectifyMap(newcam_mtx, dist, None, None, (1024,768), cv2.CV_32FC1)
    img = cv2.remap(image, map1 ,map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101, borderValue=None) 
    return img

###########################################End of Camera Calibration######################################################################
###########################################Region of Interest#############################################################################

def ROI_image(img,gray):
    ROI1= np.array([[0,50],[80,50],[80,150],[0,150]], dtype= np.int32)
    cv2.drawContours(img,[ROI1],0,(0,0,255),2)
    ROI2= np.array([[900,100],[1000,100],[1000,200],[900,200]], dtype= np.int32)
    cv2.drawContours(img,[ROI2],0,(0,0,255),2)
    ROI3= np.array([[0,630],[80,630],[80,720],[0,720]], dtype= np.int32)
    cv2.drawContours(img,[ROI3],0,(0,0,255),2)
    ROI4= np.array([[920,650],[1000,650],[1000,730],[920,730]], dtype= np.int32)
    cv2.drawContours(img,[ROI4],0,(0,0,255),2)
    blank= np.zeros_like(gray)
    region_of_interest1 = cv2.fillPoly(blank, [ROI1], 255)
    region_of_interest2 = cv2.fillPoly(region_of_interest1, [ROI2], 255)
    region_of_interest3 = cv2.fillPoly(region_of_interest2, [ROI3], 255)
    region_of_interest4 = cv2.fillPoly(region_of_interest3, [ROI4], 255)
    region_of_interest_image= cv2.bitwise_and(gray, region_of_interest4)
    return region_of_interest_image

###########################################End of Region of Interest######################################################################
###########################################Find WorkSpace#################################################################################

def Find_WorkSpace(detected_circles,calibrated_image):
    global x1, x2, x3, x4, y1, y2, y3, y4,width,height
    detected_circles = np.round(detected_circles[0, :]).astype("int")
    for (x, y, r) in detected_circles:
        if x<512 and y<384:
            x1=x
            y1=y
        if x>512 and y<384:
            x2=x
            y2=y
        if x>512 and y>384:
            x3=x
            y3=y
        if x<512 and y>384:
            x4=x
            y4=y
        dstPts = [[0, 0], [width, 0], [width, height], [0, height]]
        workspace = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        workspace = np.float32(workspace)
        m = cv2.getPerspectiveTransform(np.float32(workspace), np.float32(dstPts))
        out = cv2.warpPerspective(calibrated_image, m, (int(width), int(height)))
        #print("shape ",out.shape)
        cv2.circle(calibrated_image, (x, y), r, (0, 255, 0), 4)
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(calibrated_image, (x, y), 1, (0, 0, 255), 3)
        #cv2.circle(out, (2, 2), 1, (255, 0, 255), 3)
        image_shapes_included = out.copy()
        gray2 = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    return image_shapes_included,gray2

###########################################End of Find WorkSpace##########################################################################
###########################################End of Find WorkSpace##########################################################################

def Rack_threshold(blur,threshold_method_selector=0):
    if threshold_method_selector == 0:
        Threshold_rack = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,191, 5)
    elif threshold_method_selector == 1:
        Threshold_rack = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 191, 5)
    elif threshold_method_selector == 2:
        _, Threshold_rack = cv2.threshold(blur, 120, 220, cv2.THRESH_BINARY)
    return Threshold_rack

###########################################End of Find WorkSpace##########################################################################
###########################################Rack Properties################################################################################

def Find_Rack_Properties(cnt,gray2,image_shapes_included):
    global C,x_rack,y_rack
    x,y,w,h = cv2.boundingRect(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(image_shapes_included,[box],0,(0,0,255),2)
    #calculate kx and ky
    wx = math.sqrt(math.pow( box.ravel()[0]-box.ravel()[2],2)+math.pow( box.ravel()[1]-box.ravel()[3],2)) 
    hy = math.sqrt(math.pow( box.ravel()[2]-box.ravel()[4],2)+math.pow( box.ravel()[3]-box.ravel()[5],2))
    Wcam=max(wx,hy)/C
    Hcam=min(wx,hy)/C
    W_Rack_mm = x_rack/Wcam
    H_Rack_mm = y_rack/Hcam
    rate_mean = mean([W_Rack_mm,H_Rack_mm])
    #X_center_rack = x + w/2
    #Y_center_rack = y + h/2
    X_center_cam = np.shape(gray2)[1]/2
    Y_center_cam = np.shape(gray2)[0]/2
    cv2.putText(image_shapes_included, f"W={int(wx/(C*W_Rack_mm))},H={int(hy/(C*H_Rack_mm))}", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
    return box,W_Rack_mm,H_Rack_mm ,X_center_cam,Y_center_cam , rate_mean

###########################################End of Rack Properties#########################################################################
###########################################End of Rack ROI################################################################################

def ROI_Rack(box,gray2):
    ROI= np.array([box], dtype= np.int32)
    blank= np.zeros_like(gray2)
    region_of_interest = cv2.fillPoly(blank, ROI,255)
    region_of_interest_image= cv2.bitwise_and(gray2, region_of_interest)
    return region_of_interest_image

###########################################End of Rack ROI################################################################################
###########################################End of Rack ROI################################################################################

def Tube_threshold(region_of_interest_image,threshold_method_selector=1):
    global w3
    blur_rack = cv2.GaussianBlur(region_of_interest_image, (3, 3),0) #97 81
    threshold_num = int((w3.get())*2) + 1
    #print(threshold_num)
    if threshold_method_selector == 0:
        _, Threshold_tube = cv2.threshold(blur_rack, 120, 255, cv2.THRESH_BINARY)
    elif threshold_method_selector == 1:
        Threshold_tube = cv2.adaptiveThreshold(blur_rack,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,threshold_num,5) #comment 199 191
    elif threshold_method_selector == 2:
        _, Threshold_tube = cv2.threshold(blur_rack, 120, 220, cv2.THRESH_BINARY)
    return Threshold_tube                 

###########################################End of Rack ROI################################################################################
###########################################Detect tubes Using pixels mean color###########################################################

def Detect_tubes_Using_pixels_mean_color(gray,img,x,y,r,method = 0):
    if method == 0:
        #gray mean color of pixels 
        mean_calc_img = gray.copy()
        circle_img = np.zeros((mean_calc_img.shape[0],mean_calc_img.shape[1]), np.uint8)
        cv2.circle(circle_img,(int(x), int(y)), int(r),(255,255,255),-1)
        datos_rgb = cv2.mean(mean_calc_img, mask=circle_img)
        mean_gray = datos_rgb[0]
    elif method == 1:
        #Colorful mean color of pixels 
        mean_calc_img = img.copy()
        circle_img = np.zeros((mean_calc_img.shape[0],mean_calc_img.shape[1]), np.uint8)
        cv2.circle(circle_img,(int(x), int(y)), int(r),(255,255,255),-1)
        datos_rgb = cv2.mean(mean_calc_img, mask=circle_img)
        mean_blue = datos_rgb[0]
        mean_green = datos_rgb[1]
        mean_red = datos_rgb[2]
    #print('mean=',datos_rgb)
    #print('area=',area,'\n','r=',r)
    mean_blue = 0
    mean_red = 0
    mean_green = 0
    return mean_gray,mean_blue,mean_green,mean_red,circle_img,mean_calc_img 

###########################################End of Detect tubes Using pixels mean color####################################################
###########################################Tube location finder###########################################################################

def Tube_loc_finder(gray,img,cnts,X_center_cam,Y_center_cam,W_Rack_mm,H_Rack_mm,image_shapes_included,area,method_of_detection=1,x_y_finding_method=2):  
    global w1,w2,C,x_upper_left,y_upper_left,H,z_rack,x0,y0
    count = 0
    cordinate = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        ratio = w/h
        ((x, y), r) = cv2.minEnclosingCircle(c)
        mean_gray,mean_blue,mean_green,mean_red,circle_img,mean_calc_img = Detect_tubes_Using_pixels_mean_color(gray,img,x,y,r,method = 0)
        if ratio > .85 and ratio < 1.20 and area > 100 and area < 1000 and r < 500 and mean_gray<130 and method_of_detection == 0:
            cv2.circle(image_shapes_included, (int(x), int(y)), int(r), (36, 255, 12), -1)
            count += 1
            #print('mean=',datos_rgb)
            if x_y_finding_method == 0:
                xcm = ((x-X_center_cam))/C*W_Rack_mm -x_upper_left+(X_center_cam/C)
                ycm = y_upper_left + ((y-Y_center_cam))/C*H_Rack_mm -(Y_center_cam/C)
            elif x_y_finding_method == 1:
                xcm = ((((x-int(X_center_cam)))*H-z_rack)/H -C*x_upper_left+X_center_cam)/C
                ycm = y_upper_left + ((y-Y_center_cam))*(H-z_rack)/C*H -(Y_center_cam/C)
            elif x_y_finding_method == 2:
                xcm=(x/C)+ x_upper_left
                ycm=y_upper_left-(y/C)
            elif x_y_finding_method == 3:
                xcm=((x-2048/C)*(H-z_rack)/H+ x_upper_left)-78
                ycm=((y_upper_left-(y-1536/C)*(H-z_rack)/H)-34)/3.6
            cv2.putText(image_shapes_included, f"X={int(x)}", (int(x-r/2), int(y-r/2)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2) ## comment xcm instead of x
            cv2.putText(image_shapes_included, f"Y={int(y)}", (int(x-r/2), int(y+r/2)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2) ## comment ycm instead of y
            d = math.sqrt((int(xcm)-x0)**2+(int(ycm)-y0)**2)
            cord = pd.DataFrame({'x':[xcm] , 'y':[ycm] , 'r':[r/C] , 'd':[d/C]})
            if count==1:
                cordinate = cord
            elif count!=1:
                cordinate = pd.concat([cord,cordinate], ignore_index=True)
        if r> w1.get() and r < w2.get() and method_of_detection == 1:
            cv2.circle(image_shapes_included, (int(x), int(y)), int(r), (36, 255, 12), -1)
            count += 1
            #print('mean=',datos_rgb)
            if x_y_finding_method == 0:
                xcm = ((x-X_center_cam))/C*W_Rack_mm -x_upper_left+(X_center_cam/C)
                ycm = y_upper_left + ((y-Y_center_cam))/C*H_Rack_mm -(Y_center_cam/C)
            elif x_y_finding_method == 1:
                xcm = ((((x-int(X_center_cam)))*H-z_rack)/H -C*x_upper_left+X_center_cam)/C
                ycm = y_upper_left + ((y-Y_center_cam))*(H-z_rack)/C*H -(Y_center_cam/C)
            elif x_y_finding_method == 2:
                xcm=(x/C)+ x_upper_left
                ycm=y_upper_left-(y/C)
            elif x_y_finding_method == 3:
                xcm=((x-2048/C)*(H-z_rack)/H+ x_upper_left)-78
                ycm=((y_upper_left-(y-1536/C)*(H-z_rack)/H)-34)/3.6
            d = math.sqrt((int(xcm)-x0)**2+(int(ycm)-y0)**2)
            cord = pd.DataFrame({'count':[count],'x':[x] , 'y':[y] , 'r':[r/C] , 'd':[d/C]}) #comment xcm ycm
            if count==1:
                cordinate = cord
                cv2.putText(image_shapes_included, f"X={int(x)}", (int(x-r), int(y-r/2)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1) ## comment xcm instead of x
                cv2.putText(image_shapes_included, f"Y={int(y)}", (int(x-r), int(y)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1)
                cv2.putText(image_shapes_included, f"C={int(count)}", (int(x-r), int(y+r/2)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1)
                
            elif count!=1:
                if(check_distance_circles(cord,cordinate)):
                    cv2.putText(image_shapes_included, f"X={int(x)}", (int(x-r), int(y-r/2)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1) ## comment xcm instead of x
                    cv2.putText(image_shapes_included, f"Y={int(y)}", (int(x-r), int(y)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1)
                    cv2.putText(image_shapes_included, f"C={int(count)}", (int(x-r), int(y+r/2)), cv2.QT_FONT_NORMAL, 0.4, (255, 0, 0), 1) ## comment xcm instead of x
                    cordinate = pd.concat([cord,cordinate], ignore_index=True)

    return cordinate,count

###########################################End of Tube location finder####################################################################


###########################################Show image#####################################################################################

def show_image(detected_circles,calibrated_image,region_of_interest_image,image_shapes_included,imagedetected,Threshold_rack,Threshold_tube):
    if detected_circles is not None:
        cv2.imshow("Detected Circle", calibrated_image)
        #cv2.imshow('ds32', out)
        #cv2.imshow("ROI", region_of_interest_image)
        cv2.imshow('region of interest', region_of_interest_image)
        cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Resize", 1900, 1000)
        cv2.imshow("Resize",image_shapes_included)
        cv2.imshow("shapes", image_shapes_included)
        cv2.imshow("image detected", imagedetected)
        cv2.imshow("Threshold_rack", Threshold_rack)
        cv2.imshow("Threshold_tube", Threshold_tube)
    else:
        cv2.imshow("Detected Circle", calibrated_image)
        #cv2.imshow('ds32', out)
        #cv2.imshow("ROI", region_of_interest_image)
        cv2.imshow('region of interest', region_of_interest_image)
        cv2.imshow("shapes", image_shapes_included)
        #cv2.imshow("Threshold", threshold)
        cv2.imshow("image detected", imagedetected)

###########################################End of Show image##############################################################################
###########################################distance Measurement##############################################################################

def check_distance_circles(last_cord,list_cord):
    for i in range(list_cord.shape[0]):
        distance = math.sqrt((int(last_cord.x[0])-int(list_cord.x[i]))**2+(int(last_cord.y[0])-int(list_cord.y[i]))**2)
        if(distance < 2*last_cord.r[0]):
            # print("two near circles")
            return False
        else:
            pass
    return True             


###########################################End of distance Measurement##############################################################################



###########################################Main Code######################################################################################

def my_mainloop():
    global x1, x2, x3, x4, y1, y2, y3, y4 ,region_of_interest_image,imagedetected,Threshold_tube ,image,width,height
    _ , img = image.read()
    
    ###############
    calibrated_image = camera_calibration(img)   
    ###############
    gray = cv2.cvtColor(calibrated_image, cv2.COLOR_BGR2GRAY)
    out = np.full((width,height,3), 12, np.uint8)
    image_shapes_included = np.zeros_like(gray)
    # find 4 corners 
    region_of_interest_image = ROI_image(calibrated_image,gray)
    detected_circles = cv2.HoughCircles(region_of_interest_image,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=15,maxRadius=40) 
# Draw corners circles 
    if detected_circles is not None:
        image_shapes_included,gray2 = Find_WorkSpace(detected_circles,calibrated_image)
        blur = cv2.GaussianBlur(gray2, (81, 81),0) #97 81
        #apply threshold
        Threshold_rack = Rack_threshold(blur,threshold_method_selector=w5.get())
        contours, _ = cv2.findContours(Threshold_rack, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True) #comment 0.05
            if len(approx) == 4 and area > 5 : #comment 7000
                box,W_Rack_mm,H_Rack_mm ,X_center_cam,Y_center_cam , rate_mean = Find_Rack_Properties(cnt,gray2,image_shapes_included)
                #print('area=',area) #area3500
                #print('box=',box)
                #print('W_rack_mm=',wx*rate_mean/C)
                #print('H_rack_mm=',hy*rate_mean/C)
                #declare ROI
                region_of_interest_image = ROI_Rack(box,gray2)
                #check is there any pipe in ROI ?
                Threshold_tube = Tube_threshold(region_of_interest_image,threshold_method_selector=w4.get())
                cnts = cv2.findContours(Threshold_tube, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if len(cnts) == 2 else cnts[1]
                # cv2.imshow("region_of_interest_image", region_of_interest_image)
                cv2.namedWindow("Detected Tubes")
                cv2.setMouseCallback("Detected Tubes", click_event, param=(image_shapes_included , region_of_interest_image))
                
                # cordinate,count = Tube_loc_finder(gray,img,cnts,X_center_cam,Y_center_cam,W_Rack_mm,H_Rack_mm,image_shapes_included,area,method_of_detection=1,x_y_finding_method=2)  
                # if count >=1:
                #     # print('Count: {}'.format(count))
                #     # print('\n',cordinate)
                #     #cordinate = np.array(cordinate)
                #     imagedetected = image_shapes_included.copy()
                #     cordinate_sorted = cordinate.sort_values(by=['d'])
                #     cordinate_sorted = np.array(cordinate_sorted)
                #     # print('\n',cordinate_sorted)
                #     #print(type(cordinate_sorted))
                
                        
                
        # show_image(detected_circles,calibrated_image,region_of_interest_image,image_shapes_included,imagedetected,Threshold_rack,Threshold_tube)
        master.after(20, my_mainloop)  # run again after 1000ms (1s)
    else:
        # print("here")
        # Threshold_tube = np.zeros((200,200))
        # show_image(detected_circles,calibrated_image,region_of_interest_image,image_shapes_included,imagedetected,Threshold_rack,Threshold_tube)
        master.after(20, my_mainloop)  # run again after 1000ms (1s)



###########################################End of Main Code###############################################################################



try:
    master.after(20, my_mainloop) # run first time after 1000ms (1s)
    master.mainloop()
except KeyboardInterrupt:
    print("salam")
    cv2.destroyAllWindows()