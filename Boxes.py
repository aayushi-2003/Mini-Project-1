import cv2
import numpy as np
class RectBox:
    def __init__(self, x, y, w, h, color, text='', alpha=0.5):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.alpha = alpha
# img, textcolor, bgcolor, alpha, fontstyle, fontscale thickness
    def drawRect(self, img, text_color=(255, 255, 255), fontStyle=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2):
        alpha = self.alpha
        bg_roi = img[self.y: self.y + self.h, self.x: self.x + self.w]
        whiteRect = np.ones(bg_roi.shape, dtype=np.uint8)
        whiteRect[:] = self.color
        # blending this white rectangle with original rectangle -> adds transparency
        resImg = cv2.addWeighted(bg_roi, alpha, whiteRect, 1 - alpha, 1.0)

        img[self.y: self.y + self.h, self.x: self.x + self.w] = resImg

        text_size = cv2.getTextSize(self.text, fontStyle, fontScale, thickness)
        text_pos = (int(self.x + self.w / 2 - text_size[0][0] / 2), int(self.y + self.h / 2 + text_size[0][1] / 2))
        cv2.putText(img, self.text, text_pos, fontStyle, fontScale, text_color, thickness)

    def onButton(self, x, y):
        return ((self.x + self.w > x > self.x) and
                (self.y < y < self.y + self.h))