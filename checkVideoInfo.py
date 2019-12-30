import cv2

vcap = cv2.VideoCapture("1") # 0=camera
ret,frame = vcap.read()
print(frame)
if vcap.isOpened(): 
    width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    #print(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT) # 3, 4

    # or
    width  = vcap.get(3) # float
    height = vcap.get(4) # float

    print('width, height:', width, height)

    fps = vcap.get(cv2.CAP_PROP_FPS)
    print('fps:', fps)  # float
    #print(cv2.CAP_PROP_FPS) # 5

    fps = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('frames count:', fps)  # float
    #print(cv2.CAP_PROP_FRAME_COUNT) # 7
vcap.release()