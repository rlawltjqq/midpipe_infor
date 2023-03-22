import cv2
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.holistic
hands = mp_hands.Holistic(static_image_mode=True, )

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.left_hand_landmarks:
        for hand_landmarks in results.left_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            keypoint_pos = []
            for i in range(21):
                x = hand_landmarks.landmark[i].x * frame.shape[1]
                y = hand_landmarks.landmark[i].y * frame.shape[0]
                keypoint_pos.append((x, y))

    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()