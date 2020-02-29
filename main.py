import cv2
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
# reading image
img = cv2.imread(img_path)
img = cv2.resize(img, (600, 400))

# or use cv2.imread('image name')
# img = cv2.imread('BKNA.jpg')
# img = cv2.resize(img, (400, 400))

# global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# reading the csv file with pandas
# and giving names to each coloumn
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv_file = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate the minimum distance from all
# the colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv_file)):
        d = abs(R-int(csv_file.loc[i, 'R']))+abs(G-int(csv_file.loc[i, 'G']))+abs(B-int(csv_file.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            colorname = csv_file.loc[i, 'color_name']
    return colorname


# function to get x,y coordinates of mouse click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(background image, startpoint, endpoint, color, thickness)
        # -1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        # Creating text string to display color name
        text = get_color_name(r, g, b)
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    # press 'esc' to break the loop
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()