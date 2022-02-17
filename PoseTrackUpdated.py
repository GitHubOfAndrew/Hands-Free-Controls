# THIS SCRIPT WILL CONTAIN THE INNER WORKINGS OF OUR PROJECT, THE POSE TRACKING

# IMPORT DEPENDENCIES
import cv2 as cv2
import mediapipe as mp
import time
import numpy as np

# CREATE POSE DETECTOR OBJECT

class pose_detector():
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_confidence=0.5, track_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        # landmark id of the finger tips
        self.fingertip_id = [4, 8, 12, 16, 20]
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity,
                                         self.detection_confidence,self.track_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    # FIND HANDS AND RETURN THE IMAGE WITH THE LANDMARKS MARKED
    def find_hands(self, frame, draw=True):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process
        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            # draw points on landmarks of hands
            for handlmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, handlmark, self.mp_hands.HAND_CONNECTIONS)
        return frame

    # FIND POSITION OF LANDMARKS OF HAND
    def find_position(self, frame, num_hand=0, draw=True):
        xli = []
        yli = []
        self.landmark_li = []
        bounding_box = ()
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[num_hand]
            for id, lm in enumerate(my_hand.landmark):
                height, width, channels = frame.shape
                # convert to pixels
                cx, cy = int(lm.x * width), int(lm.y * height)
                xli.append(cx)
                yli.append(cy)
                self.landmark_li.append([id, cx, cy])
                # id specifies which landmark on hand (pinky, pointer, thumb, etc) is being tracked
                if draw:
                    cv2.circle(frame, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xli), max(xli)
            ymin, ymax = min(yli), max(yli)
            bounding_box = xmin, ymin, xmax, ymax
            # print(self.results.multi_hand_landmarks)
            if draw:
                cv2.rectangle(frame, (bounding_box[0]-20, bounding_box[1]-20), (bounding_box[2]+20, bounding_box[3]+20), (0, 255, 0), 2)
        return self.landmark_li, bounding_box

    # TRACK IF FINGERS ARE UP OR DOWN
    def fingers_up(self):
        fingers = []
        # see if thumb is up or down
        if self.landmark_li[self.fingertip_id[0]][1] < self.landmark_li[self.fingertip_id[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # other 4 fingers
        for lm_id in range(1,5):
            if self.landmark_li[self.fingertip_id[lm_id]][2] < self.landmark_li[self.fingertip_id[lm_id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def find_distance(self, pt1, pt2, img, draw=True):
        x1, y1 = self.landmark_li[pt1][1], self.landmark_li[pt1][2]
        x2, y2 = self.landmark_li[pt2][1], self.landmark_li[pt2][2]
        # midpoint between the landmarks
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 135), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 135), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            # mark midpoint
            cv2.circle(img, (cx, cy), 7, (0, 0, 255), cv2.FILLED)

        length_1 = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return length_1, img, [x1, y1, x2, y2, cx, cy]

def main():
    ptime, ctime = 0, 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = pose_detector()
    while (cap.isOpened()):
        ret, frame = cap.read()
        frame = detector.find_hands(frame)

        # find position on right hand
        landmark_li_1, bounding_box = detector.find_position(frame)
        if landmark_li_1:
            print(landmark_li_1)
        else:
            pass

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        img_final = cv2.flip(frame, 1)
        cv2.putText(img_final, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 255), 2)
        cv2.imshow('Frame', img_final)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
