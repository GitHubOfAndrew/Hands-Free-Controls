# THIS SCRIPT WILL CONTROL BRIGHTNESS THROUGH HANDS-FREE METHODS

# IMPORT BRIGHTNESS CONTROL
import screen_brightness_control as sbc

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

min_brightness = 5
max_brightness = 100
brightness_bar = 50
brightness_percent = 5
area_bb = 0
# make volume text color blue
brightness_color = (255,0,0)

while (cap.isOpened()):
    ret, frame = cap.read()
    frame_flip = cv2.flip(frame, 1)
    img = detector.find_hands(frame_flip)
    lmark_li, bounding_box = detector.find_position(img)
    flag_set_vol = False
    if lmark_li:
        # print(lmark_li[4], lmark_li[8])

        # FILTER HAND CONTROL SO THAT WE CAN MAINTAIN CONSISTENCY IN VOLUME OUTPUT
        # find area of bounding box
        area_bb = (bounding_box[2] - bounding_box[0])*(bounding_box[3] - bounding_box[1])//100
        print(area_bb)
        if area_bb < 900 and area_bb > 300:
            print('Valid Range')
            # BRIGHTNESS CONTROL
            # have landmark 4 (thumb) and landmark 8 (index) marked
                        # print(length)
            length_1, img, coordinates = detector.find_distance(4, 8, img)
            # print(length_1)

            # shift the scale of our volume control
            brightness_bar = np.interp(length_1, [30, 175], [50, 175])
            brightness_percent = np.interp(length_1, [30, 175], [5, 100])

            # smoothness is the increment we will increase volume at, have it higher for smoothness,
            # lower for less smoothness but more granular volume control
            brightness_smoothness = 4
            brightness_percent = brightness_smoothness*round(brightness_percent/brightness_smoothness)

            # track which fingers are up or down
            fingers = detector.fingers_up()
            # print(fingers)

            # when middle finger goes down, set the brightness at what it is
            if fingers[-3] == 0:
                sbc.set_brightness(brightness_percent)
                # while brightness is being changed, we make the midpoint circle green, and make the counter green
                # green is an indication that we are active in our changes
                cv2.circle(img, (coordinates[4], coordinates[5]), 7, (0, 255, 0), cv2.FILLED)
                brightness_color = (0, 255, 0)
                if length_1 < 30:
                    cv2.circle(img, (coordinates[4], coordinates[5]), 7, (200, 0, 0), cv2.FILLED)
            else:
                # when volume is not being changed, turn to blue
                brightness_color = (255, 0, 0)
            # cv2.circle(img, (coordinates[4], coordinates[5]), 7, (0, 200, 0), cv2.FILLED)
            # make a "button" for when we have our fingers together so we know we hit minimum
            if length_1 < 30:
                cv2.circle(img, (coordinates[4], coordinates[5]), 7, (200, 0, 0), cv2.FILLED)
            # test ranges: we had about 30 - 210 comfortably
            # volume range: -65 - 0
        else:
            pass

    # make our own volume bar and add to UI
    cv2.rectangle(img, (50, 430), (175, 460), (255, 127, 0), 3)
    cv2.rectangle(img, (50, 430), (int(brightness_bar), 460), (255, 127, 0), cv2.FILLED)
    if sbc.get_brightness == 5:
        cv2.rectangle(img, (50, 430), (175, 460), (255, 127, 0), cv2.FILLED)
    if sbc.get_brightness == 100:
        cv2.rectangle(img, (50, 430) , (50, 460), (255, 127, 0), cv2.FILLED)
    cv2.putText(img, f'{int(brightness_percent)} %', (55, 450), cv2.FONT_HERSHEY_PLAIN,
                1, (192, 192, 192), 2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    # img_final = cv2.flip(frame, 1)
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 255), 2)

    # display volume
    display_brightness = sbc.get_brightness()
    if sbc.get_brightness() == 5:
        brightness_color = (0,0,255)
    if sbc.get_brightness() == 100:
        brightness_color = (255,0,0)
    cv2.putText(img, f'Brightness: {display_brightness}', (10, 140), cv2.FONT_HERSHEY_PLAIN,
                3, brightness_color, 2)
    cv2.imshow('Frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()