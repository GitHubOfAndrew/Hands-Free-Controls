# THIS SCRIPT WILL ALLOW HANDS-FREE CONTROL OF OUR VOLUME

# IMPORT DEPENDENCIES
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
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

# INITIALIZE AUDIO OUTPUTS
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange()
min_vol = volume_range[0]
max_vol = volume_range[1]
vol_bar = 50
vol_percent = 0
area_bb = 0
# make volume text color blue
volume_color = (255,0,0)

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
            # VOLUME CONTROL
            # have landmark 4 (thumb) and landmark 8 (index) marked
                        # print(length)
            length_1, img, coordinates = detector.find_distance(4, 8, img)
            # print(length_1)

            # shift the scale of our volume control
            vol_bar = np.interp(length_1, [30, 175], [50, 175])
            vol_percent = np.interp(length_1, [30, 175], [0, 100])

            # smoothness is the increment we will increase volume at, have it higher for smoothness,
            # lower for less smoothness but more granular volume control
            vol_smoothness = 4
            vol_percent = vol_smoothness*round(vol_percent/vol_smoothness)

            # track which fingers are up or down
            fingers = detector.fingers_up()
            # print(fingers)

            # set volume to scale linearly instead of logarithmically
            # when pinky goes down, set the volume at what it is
            count = 0
            if fingers[-3] == 0:
                volume.SetMasterVolumeLevelScalar(vol_percent / 100, None)
                # while volume is being changed, we make the midpoint circle green, and make the volume counter green
                # green is an indication that we are active in our changes
                cv2.circle(img, (coordinates[4], coordinates[5]), 7, (0, 255, 0), cv2.FILLED)
                volume_color = (0, 255, 0)
                if length_1 < 30:
                    cv2.circle(img, (coordinates[4], coordinates[5]), 7, (200, 0, 0), cv2.FILLED)
            else:
                # when volume is not being changed, turn to blue
                volume_color = (255, 0, 0)
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
    cv2.rectangle(img, (50, 430), (int(vol_bar), 460), (255, 127, 0), cv2.FILLED)
    if volume.GetMasterVolumeLevel() == 0.0:
        cv2.rectangle(img, (50, 430), (175, 460), (255, 127, 0), cv2.FILLED)
    if volume.GetMasterVolumeLevel() == -65.25:
        cv2.rectangle(img, (50, 430) , (50, 460), (255, 127, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol_percent)} % Volume', (55, 450), cv2.FONT_HERSHEY_PLAIN,
                1, (192, 192, 192), 2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    # img_final = cv2.flip(frame, 1)
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 255), 2)

    # display volume
    display_vol = int(volume.GetMasterVolumeLevelScalar()*100)
    if volume.GetMasterVolumeLevel() == 0.0:
        volume_color = (0,0,255)
    if volume.GetMasterVolumeLevel() == -65.25:
        volume_color = (255,0,0)
    cv2.putText(img, f'Vol: {display_vol}', (10, 140), cv2.FONT_HERSHEY_PLAIN,
                3, volume_color, 2)
    cv2.imshow('Frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()