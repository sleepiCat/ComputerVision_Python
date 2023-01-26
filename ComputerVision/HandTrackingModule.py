import cv2
import mediapipe as mp
import time


class HandDetector:

    def __init__(self, mode=False, max_hands=2, model_complex=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complex = model_complex
        self.detectionCon = detection_con
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.model_complex,
                                        self.detectionCon, self.trackCon)
        # connects the finger joints with class drawing_utils
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # draw_landmarks method(img, each joint location, connections between joints)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPostion(self, img, handNo=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:
            handLms = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(handLms.landmark):
                #lm: [x: val, y: val, z: val]
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append(id, cx, cy)
                #specific joint location is id
                #if id == 4:
                if draw:
                    cv2.circle(img, (cx, cy), 15, (200, 0, 100), cv2.FILLED)

        return lmList
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()

        detector = HandDetector()
        img = detector.findHands(img, True)
        #lms = detector.findPostion(img)
        #if lms:
        #    print(lms[4])

        # calculate fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


#starting point of this script
if __name__ == "__main__":
    main()
