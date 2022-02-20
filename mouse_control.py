# THIS SCRIPT WILL ALLOW HANDS-FREE CONTROL OF OUR VOLUME

# IMPORT MOUSE CONTROLS
from pynput.mouse import Button, Controller

# IMPORT SCREEN RESOLUTION SETTINGS
import tkinter

# IMPORT BASE DEPENDENCIES
import cv2 as cv2
import time
import numpy as np
import PoseTrackUpdated as PT

# cam settings
w, h = 640, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, w)
cap.set(4, h)

ptime, ctime = 0, 0
detector = PT.pose_detector(detection_confidence=0.7, max_hands=1)

# INITIALIZE MOUSE INPUT
mouse = Controller()

# INITIALIZE SCREEN SPECIFICATIONS
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

# INITIALIZE BOUNDING BOX AREA
area_bb = 0

while cap.isOpened():
    ret, frame = cap.read()
    frame_flip = cv2.flip(frame, 1)
    img = detector.find_hands(frame_flip)
    lmark_li, bounding_box = detector.find_position(img)
    flag_set_vol = False
    if lmark_li:
        # print(lmark_li[5], lmark_li[8])

        # FILTER HAND CONTROL SO THAT WE CAN MAINTAIN CONSISTENCY IN VOLUME OUTPUT
        # find area of bounding box
        area_bb = (bounding_box[2] - bounding_box[0])*(bounding_box[3] - bounding_box[1])//100
        print('The bounding box area is:', area_bb)
        if area_bb < 900 and area_bb > 0:
            print('Valid Range')

            # TRACK CURSOR: GET COORDINATES OF LANDMARK OF CHOICE TO USE AS OUR CURSOR
            # here: we are trying the thumb as a cursor so that we can possibly use index and middle finger
            # as left and right click
            # OUR CURSOR POSITION THROUGH THE CAMERA
            cursor_x, cursor_y = lmark_li[4][1], lmark_li[4][2]
            print(cursor_x, cursor_y)

            # interpolate the cursor position according to the size of our webcam window into
            # the total resolution of our screen (this will require some testing)
            # OUR PROJECTED CURSOR POSITION ON THE ACTUAL DISPLAY
            cursor_position_x = np.interp(cursor_x, [60, 400], [0, WIDTH])
            cursor_position_y = np.interp(cursor_y, [130, 300], [0, HEIGHT])
            # print(cursor_position_x, cursor_position_y)

            # adjust coordinates of the cursor according to the interpolated cursor position
            mouse.position = (cursor_position_x, cursor_position_y)

            # print(mouse.position)
            # # track which fingers are up or down
            fingers = detector.fingers_up()
            print(fingers)
            # CLICK CURSOR: IMPLEMENT RIGHT CLICK AND LEFT CLICK
            if fingers[1] == 0:
                # this is the index finger action for left click, release once finger goes back up
                mouse.press(Button.left)
                mouse.release(Button.left)
            if fingers[2] == 0:
                # this is the middle finger action for right click, release once finger goes back up
                mouse.press(Button.right)
                mouse.release(Button.right)
        else:
            print('Out of Range: please take your hand further away')


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    # img_final = cv2.flip(frame, 1)
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 255), 2)

    cv2.imshow('Frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()