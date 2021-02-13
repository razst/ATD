import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import imutils
import faceRec


def main():
    print("Init face rec engine...")
    fr = faceRec.FaceRec()
    print("Done init face rec engine...")

    drone = tellopy.Tello()
    
    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        retry = 3
        container = None
        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')
        
        start = time.time()
        frameCount=0
        fps=0

        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                image = imutils.resize(image, width=500) # for tello, 500 is the max we can have without too many frame drops, and skip frames = 1
                image = fr.processFrame(image)

                frameCount = frameCount + 1
                now = time.time()
                if now-start>=1:              
                    fps=frameCount/(now-start) 
                    print("From WbCam FPS: {:.2f}".format(fps))
                    frameCount=0
                    start = time.time()

                start_time = time.time()
                cv2.waitKey(1)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
                    

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        print("Stopping threads...")
        fr.stop()
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()