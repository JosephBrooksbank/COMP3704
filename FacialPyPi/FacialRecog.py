

from imutils.video import VideoStream
import time
import dlib
import cv2


# Loading facial detector from dlib, a toolkit containing a good facial detection algorithm 
detector = dlib.get_frontal_face_detector()

# Grab video stream from pi camera
vs = VideoStream(usePiCamera=True).start()
# camera takes a bit of time to turn on, so giving it some time here
time.sleep(2.0)

# print("Starting detection:")

while True:

    # reading frame, converting to grayscale for face detection
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # grabbing facial frames
    rects = detector(gray, 0)
    if len(rects) == 0:
        print("no face detected")
        time.sleep(0.5)
    else:
        print("face detected!")
        time.sleep(0.5)