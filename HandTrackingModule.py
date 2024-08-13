import cv2
import mediapipe as mp
import time
import math
import autopy
from cvzone import handTrackingModule as HandModule

class handDetector(HandModule):
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        super().__init__(mode, maxHands, detectionCon, trackCon)

    def findHands(self, img, draw=True):
        img = super().findHands(img, draw=draw)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList, bbox = super().findPosition(img, handNo=handNo, draw=draw)
        return lmList, bbox

    def fingersUp(self):
        fingers = super().fingersUp()
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        length, img, lineInfo = super().findDistance(p1, p2, img, draw=draw, r=r, t=t)
        return length, img, lineInfo


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
