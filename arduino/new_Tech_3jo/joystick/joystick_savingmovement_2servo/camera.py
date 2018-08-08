import argparse
import datetime
import imutils
import time
import cv2
from imutils.object_detection import non_max_suppression
from imutils import paths
from PIL import Image, ImageEnhance
import numpy as np

vidcap = cv2.VideoCapture(0)
Framewidth = 600
kernel = np.ones((3,3),np.uint8)

firstframe = None

(grabbed, frame) = vidcap.read()
if grabbed:
    frame = imutils.resize(frame, width=Framewidth)
    inWidth = frame.shape[1]
    inHeight = frame.shape[0]
    WHRatio = inWidth / float(inHeight)

while True:
    # ���� ĸ�Ŀ� ���� ��ü frame ����
    (grabbed, frame) = vidcap.read()

    # ĸ�� ���н� ���α׷� ����
    if not grabbed:
        break

    frame = imutils.resize(frame, width=Framewidth)
    

    cv2.imshow("Orginal", frame)

    

    key = cv2.waitKey(1) & 0xFF
    # ESC��ư�� ���� while loop�� ���������� �����ϴ�.
    if key == 27:
        break

vidcap.release()
cv2.destroyAllWindows()
