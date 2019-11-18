

from imutils.video import VideoStream

from roku import RokuException
import time
import cv2
from roku import Roku

# time until roku shuts off, in seconds (600s = 10 minutes)
TIMEOUT = 600

roku = 0
rList = Roku.discover()
for r in rList:
    if r.port == 8060:
        roku = r
if roku == 0:
    # This terminates the program -- I handle upkeep in systemd to save resources
    raise Exception('No valid Rokus found on network')

lastSeen = time.time()

try:

    #  Loading model, I DID NOT MAKE THIS, FROM OPENCV GITHUB REPOSITORY
    net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "model.caffemodel")

    # initializing pi camera to a video stream, using a python image/video library imutils
    vs = VideoStream(usePiCamera=True).start()
    # camera takes some time to turn on, so giving it time here
    time.sleep(2.0)

    # loop over the frames from the video stream
    while True:
        numFaces = 0

       # getting frame
        frame = vs.read()
        # grab the frame dimensions and convert it to a blob (Binary Large OBject, pixel grouping detection)
        (h, w) = frame.shape[:2]
        # parameters for blob detection taken from OpenCV's facial detection benchmarking program (see OpenCV's Github)
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # Pass blob data to dnn
        net.setInput(blob)
        # run forward pass
        detections = net.forward()

       #detector array format
       # batchId, classId, confidence, left, top, right, bottom
        ## all I really care about is confidence, I don't care WHERE the face is, only that one exists

        # loop over the detections (shape: 1,1,200,7, BASICALLY a 2D array in this case)
        for i in range(0, detections.shape[2]):

            # extract the confidence for each array entry
            confidence = detections[0, 0, i, 2]

            # if detection is less than 30% confident, ignore that detection
            if confidence < 0.3:
                continue
            numFaces += 1
            print("Face Found!")


        if numFaces > 0:
            lastSeen = time.time()
        else:
            print(str(TIMEOUT - int(time.time() - lastSeen)) + " seconds until screen off!")

            if int(time.time() - lastSeen) > TIMEOUT:
             # the roku API gives an exception every time the TV power is turned off or on -- I think it doesn't
             # send an ACK on this command, which the API doesn't like. anyway, it doesn't actually effect
             # functionality, so I'm ignoring it.
                try:
                    roku.poweroff()
                except RokuException:
                    pass
                lastSeen = time.time()

# This is a little dirty but its the best way I've found of exiting over ssh
except (KeyboardInterrupt, SystemExit):
    vs.stop()
