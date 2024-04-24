import cv2
from time import sleep
import Boxes as Rb
from HandTracking import HandTrackingMain as htm

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(detectionCon=0.8)

keys = list("QWERTYUIOPASDFGHJKLZXCVBNM")

finalText = ""
w, h = 100, 80
startX, startY = 100, 100

buttonList = []
for i, key in enumerate(keys):
    if i < 10:
        buttonList.append(Rb.RectBox(startX + i * w + i * 5, startY, w, h, (0, 0, 0), key))
    elif i < 19:
        buttonList.append(Rb.RectBox(startX + (i - 10) * w + i * 5, startY + h + 5, w, h, (0, 0, 0), key))
    else:
        buttonList.append(Rb.RectBox(startX + (i - 19) * w + i * 5, startY + 2 * h + 10, w, h, (0, 0, 0), key))

buttonList.append(Rb.RectBox(startX + 25, startY + 3 * h + 15, 5 * w, h, (0, 0, 0), "Space"))
buttonList.append(Rb.RectBox(startX + 8 * w + 50, startY + 2 * h + 10, w, h, (0, 0, 0), "clr"))
buttonList.append(Rb.RectBox(startX + 5 * w + 30, startY + 3 * h + 15, 5 * w, h, (0, 0, 0), "<--"))

coolingCounter = 15


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.x, button.y
        w, h = button.w, button.h
        cv2.rectangle(img, (button.x, button.y), (button.x + button.w, button.y + button.h), (51, 26, 2), cv2.FILLED)
        cv2.putText(img, button.text, (x + 35, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img

while True:
    if coolingCounter > 0:
        # print(coolingCounter)
        coolingCounter -= 1

    success, img = cap.read()
    img = cv2.resize(img, (wCam, hCam))
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.x, button.y
            w, h = button.w, button.h
            # fingers = detector.fingersUp()
            # print(lmList[8][1])
            if button.onButton(lmList[8][1], lmList[8][2]):
                cv2.rectangle(img, (button.x, button.y), (button.x + button.w, button.y + button.h), (150, 78, 6), cv2.FILLED)
                cv2.putText(img, button.text, (x + 35, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                l, _, _ = detector.findDistance(8, 4, img, draw=False)
                print(l)

                if l < 35 and not coolingCounter:
                    coolingCounter = 15
                    cv2.rectangle(img, (button.x, button.y), (button.x + button.w, button.y + button.h), (214, 11, 8), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 35, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    if button.text == "<--":
                        finalText = finalText[:-1]
                    elif button.text == "clr":
                        finalText = ""
                    elif button.text == "Space":
                        finalText += " "
                    else:
                        finalText += button.text
                    sleep(0.15)

    cv2.rectangle(img, (startX, 600), (1140, 680), (51, 26, 2), cv2.FILLED)
    cv2.putText(img, finalText, (startX + 40, 650), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
