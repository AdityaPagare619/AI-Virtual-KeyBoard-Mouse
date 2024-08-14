import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep, time
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

frameR = 100
smoothing = 7

# Specify the detection confidence for HandDetector
detector = HandDetector(detectionCon=1, maxHands=2)

# Adjusted size for a smaller keyboard
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""
keyboard = Controller()

class Button():
    def __init__(self, pos, text, size=[30, 30]):  # Adjusted button size
        self.pos = pos
        self.size = size
        self.text = text
        self.lastClicked = 0  # Timestamp of the last click




buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        # Adjusted button positions and color
        buttonList.append(Button([90 * j + 50, 90 * i + 50], key, [70, 70]))

cooldown_time = 2.0  # Cooldown period in seconds

def drawAll(img, buttonList, finalText):
    imgNew = img.copy()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        ## todo Bg rectangle
        cv2.rectangle(img, (50, 50), (930, 460), (0, 0, 0, 31), cv2.FILLED)
        cv2.rectangle(img, (50, 50), (930, 460), (0, 0, 0), 15)
        cv2.circle(imgNew, (x + int(w / 2), y + int(h / 2)), int(w / 2), (31, 31, 31, 1), cv2.FILLED)  # Rounded background for all keys
        textSize = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        textX = int(x + (w - textSize[0]) / 2)
        textY = int(y + h / 2 + textSize[1] / 2)
        cv2.putText(imgNew, button.text, (textX, textY), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)  # White text




    # Rectangle where words will get printed
    cv2.rectangle(imgNew, (48, 370), (750, 450), (0, 0, 0, 31), cv2.FILLED)
    cv2.rectangle(imgNew, (48, 370), (750, 450), (0, 0, 0, 31), 15)
    cv2.putText(imgNew, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Overlay the keyboard on the original frame
    img = cv2.addWeighted(img, 1, imgNew, 0.7, 0)

    return img

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    if lmList:
        x, y = lmList[8]  # Tip of index finger
        for button in buttonList:
            bx, by = button.pos
            bw, bh = button.size

            # Check if tip of index finger is within the boundaries of the button
            if bx < x < bx + bw and by < y < by + bh:
                cv2.circle(img, (bx + int(bw / 2), by + int(bh / 2)), int(bw / 2), (175, 0, 175), cv2.FILLED)
                textSize = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
                textX = int(bx + (bw - textSize[0]) / 2)
                textY = int(by + bh / 2 + textSize[1] / 2)
                cv2.putText(img, button.text, (textX, textY), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)

                # when clicked and cooldown period has passed
                if l < 30 and (time() - button.lastClicked) > cooldown_time:
                    keyboard.press(button.text)
                    cv2.circle(img, (bx + int(bw / 2), by + int(bh / 2)), int(bw / 2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (textX, textY), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                    finalText += button.text
                    button.lastClicked = time()
                    sleep(0.15)

    img = drawAll(img, buttonList, finalText)

    cv2.imshow("Virtual Keyboard", img)

    # Add a delay to avoid continuous key presses
    cv2.waitKey(1)

    key = cv2.waitKey(1)
    if key == ord('Q') or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()







