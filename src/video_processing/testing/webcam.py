#Henry Kou
#Run to view camera feed



from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

print(args)

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=1).start() #src = 0 is internal webcam, src = 1 is external webcam
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	#frame = frame if args.get("video", None) is None else frame[1]
	cv2.imshow("Security Feed", frame)
	key = cv2.waitKey(1) & 0xFF
	
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break


# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()