import face_recognition
import cv2
import numpy as np
from multiprocessing import Process, Queue
import time
import queue
#1356236087

IMAGE_SHRINK_RATIO = 1 #how much to shrink the image frame, the more we shrink the more FPS we can process BUT the face must be closer to the camera!
Q_SIZE = 10
THREAD_NUM = 5
SKIP_FRAMES = 2


class FaceRec:

    pleaseStop = False
    origFrameQ=None
    finalFrameQ=None

    
    def stop(self):
        self.pleaseStop=True
    
    def detectFaces(self,frame):
        
        ret=0
        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=IMAGE_SHRINK_RATIO, fy=IMAGE_SHRINK_RATIO)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = frame[:, :, ::-1]

        # Only process every other frame of video to save time
        
        if self.process_this_frame>=SKIP_FRAMES:
            ret=1
            # Find all the faces and face encodings in the current frame of video
            
            self.face_locations = face_recognition.face_locations(rgb_small_frame, model="hog") # model="cnn" or model="hog" (faster but less accurate)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
          
            
            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)
            self.process_this_frame = 0
        else:    
            self.process_this_frame = self.process_this_frame + 1
            
        
        
        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= int(1/IMAGE_SHRINK_RATIO)
            right *= int(1/IMAGE_SHRINK_RATIO)
            bottom *= int(1/IMAGE_SHRINK_RATIO)
            left *= int(1/IMAGE_SHRINK_RATIO)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        self.finalFrameQ.put(frame)
        
        return ret
        
    def consumeOrigFrame(self,q):
        start = time.time()
        frameCount=0
        fps=0
        process_this_frame = 0
        while(self.pleaseStop != True):
            #name = threading.currentThread().getName()
            #print(name,origFrameQ.qsize())
            when, frame = q.get()
            # do processing here...
            rgb_small_frame = frame[:, :, ::-1]

            # Only process every other frame of video to save time
            
            if process_this_frame>=SKIP_FRAMES:
                frameCount = frameCount + 1
                # Find all the faces and face encodings in the current frame of video
                
                self.face_locations = face_recognition.face_locations(rgb_small_frame, model="hog") # model="cnn" or model="hog" (faster but less accurate)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
              
                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    self.face_names.append(name)
                process_this_frame = 0
            else:    
                process_this_frame = process_this_frame + 1
                
            
            
            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            self.finalFrameQ.put((when,frame))
            #frameCount = frameCount + self.detectFaces(item)
            now = time.time()
            if now-start>=5:              
                fps=frameCount/(now-start) 
                print("Proceesed FPS: {:.2f}".format(fps))
                frameCount=0
                start = time.time()

    def consumeFinalFrame(self,q):
        start = time.time()
        frameCount=0
        fps=0
        lastFrameTime=0
        while(self.pleaseStop != True):
            #name = threading.currentThread().getName()
            #print(name,finalFrameQ.qsize())
            when, frame = q.get();
            if lastFrameTime>when:
                continue
            lastFrameTime = when
            # do processing here...
            cv2.putText(frame, "Final FPS: {:.2f}".format(fps), (2, 20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)
            cv2.imshow('DJI Tello', frame)
            
            frameCount = frameCount + 1
            now = time.time()
            if now-start>=5:              
                fps=frameCount/(now-start) 
                print("Final FPS: {:.2f}".format(fps))
                frameCount=0
                start = time.time()
            # Video Stream is closed if escape key is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            #q.task_done()
            
        cv2.destroyAllWindows()

    def __init__(self):
        
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("raz1.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("uk.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        self.known_face_names = [
            "Raz",
            "Unknown"
        ]

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        
        # start al  l consumer producer threads
        self.origFrameQ = Queue(maxsize = Q_SIZE)
        self.finalFrameQ = Queue(maxsize = Q_SIZE)
        for i in range(THREAD_NUM):
            p = Process(name = "finalThread",target=self.consumeOrigFrame, args=(self.origFrameQ,))
            p.start()

        p=Process(name = "finalThread", target=self.consumeFinalFrame, args=(self.finalFrameQ,))
        p.start()

    def processFrame(self,frame):
        try:
            #print("qsize=",origFrameQ.qsize())
            self.origFrameQ.put_nowait((time.time(),frame))
            #self.finalFrameQ.put_nowait((time.time(),frame))
        except queue.Full:
            print("**** full ****")

