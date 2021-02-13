#!/usr/bin/env python
from multiprocessing import Process, Queue

from queue import Empty
from PIL import Image
import cv2
import numpy as np
import time
import faceRec


def image_display(taskqueue):
   cv2.namedWindow ('image_display', cv2.WINDOW_AUTOSIZE)
   while True:

      image = taskqueue.get()              # Added
      if image is None:  break             # Added
      cv2.imshow ('image_display', image)  # Added
      cv2.waitKey(10)                      # Added


if __name__ == '__main__':
   fr = faceRec.FaceRec()
   vidFile = cv2.VideoCapture(0)
   while True:
      flag, image=vidFile.read()       
      fr.processFrame(image)
      #taskqueue.put(image)  # Added
      time.sleep(0.010)     # Added


   taskqueue.put(None)
   p.join()
   cv.DestroyAllWindows()