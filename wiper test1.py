import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import mediapipe as mp
from dynamikontrol import Module

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap =cv2.VideoCapture(0)

module = Module()

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('not opened ffuck')
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmakrs in results.multi_hand_landmarks:
                thumb = hand_landmakrs.landmark[4] # 엄지
                index = hand_landmakrs.landmark[8] # 검지

                diff = abs(index.x - thumb.x)

                wiper = int(diff * 500) # 거리 따라 수정 
                module.motor.angle(wiper)

                cv2.putText(
                    image, text= 'angle %d' % wiper, org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                    color=255, thickness=2
                )
                mp_drawing.draw_landmarks(
                    image, hand_landmakrs, mp_hands.HAND_CONNECTIONS
                )
        cv2.imshow('wiper', image)
        if cv2.waitKey(1) == ord('esc'):
            break 
    cap.release()   