import numpy as np
import cv2 as cv

cap = cv.VideoCapture('output.avi')
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output_boxed.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([75,50,50])
    upper_blue = np.array([105,255,255])
    # Threshold the HSV image to get only blue colors   
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)


    # my edition
    if ret==True:
        sum=0
        total_num=0
        for col in range(0,480):
            num=0
            for row in range(0,640):
                if mask[col][row]!=0:
                    num=num+1
            total_num=total_num+num
            sum=sum+col*num
        if total_num!=0:
            ver_center=round(sum/total_num)
        else:
            ver_center=0

        sum=0
        total_num=0
        for row in range(0,640):
            num=0
            for col in range(0,480):
                if mask[col][row]!=0:
                    num=num+1
            total_num=total_num+num
            sum=sum+row*num
        if total_num!=0:
            hor_center=round(sum/total_num)
        else:
            hor_center=0

        if (ver_center!=0)&(hor_center!=0):
            left_edge=hor_center-75
            right_edge=hor_center+75
            up_edge=ver_center-75
            down_edge=ver_center+75

            if left_edge<0:
                left_edge=0
            if right_edge>639:
                right_edge=639
            if up_edge<0:
                up_edge=0
            if down_edge>479:
                down_edge=479

            frame[up_edge:down_edge,left_edge]=[0,0,255]
            frame[up_edge:down_edge,right_edge]=[0,0,255]
            frame[up_edge,left_edge:right_edge]=[0,0,255]
            frame[down_edge,left_edge:right_edge]=[0,0,255]

        out.write(frame)
    # end of my edition

    # cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()