import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


# my edition

img = cv2.imread("screenshots/dimmer_phone.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower_blue = np.array([75,50,50])
upper_blue = np.array([105,255,255])
# Threshold the HSV image to get only blue colors   
mask = cv2.inRange(img, lower_blue, upper_blue)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(img,img, mask= mask)


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


img_box=img[up_edge:down_edge,left_edge:right_edge]

cv2.imshow('image',img_box)




#end of my edition


img_box = img_box.reshape((img_box.shape[0] * img_box.shape[1],3)) #represent as row*column,channel number
clt = KMeans(n_clusters=3) #cluster number
clt.fit(img_box)

hist = find_histogram(clt)
bar = plot_colors2(hist, clt.cluster_centers_)

plt.axis("off")
plt.imshow(bar)

plt.show()