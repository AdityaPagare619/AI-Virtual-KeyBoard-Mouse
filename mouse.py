import cv2
import mediapipe as mp
import pyautogui

# Initialize hand tracking
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

mpHands = mp.solutions.hands
hands = mpHands.Hands()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Convert the BGR image to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe hands
    results = hands.process(rgb_img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract hand landmarks as needed

            # Get the tip of the index and middle fingers
            index_finger = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]

            # Move the mouse based on the index finger position
            screen_width, screen_height = pyautogui.size()
            x = int(index_finger.x * screen_width)
            y = int(index_finger.y * screen_height)
            pyautogui.moveTo(x, y)

            # Check if the index and middle fingers are up to perform a click
            if middle_finger.y < index_finger.y:
                pyautogui.click()

    # Display the frame
    cv2.imshow("Virtual Mouse", img)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()