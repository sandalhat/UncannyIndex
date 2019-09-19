import cv2
import numpy
import serial
from time import sleep

#use standard cascaades from the library
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#open the actual usb camera
cap = cv2.VideoCapture(0)

#report error if camera couldn't be opened or wasn't found
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#introduce count variable for counting frames, in order to only process one out of every so many frames
count = 0

#setup a serial connection for the teensy, which will run the animated eyes
result = None
while result is None:
    try:
        ser = serial.Serial('COM3', 115200)
        result = 1
    except:
        sleep(1)
        pass

#loop through, looking for faces and finding their location within the frame
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #This crops to the size of one camera on the Valve Index - won't be needed for normal cameras since the Index combines video from 2 cameras into one stream
    frame = frame[0:960,0:800]

    if count % 2 == 0: #this line is used to reduce CPU load by only running the algorithm every multiple of frames, depending on the value used in the modulo operation
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #perform the face detection and send data to python
        faces = face_cascade.detectMultiScale(gray, 1.2, 8) #the second and third arguments are the scale factor and the number of neighbors, respectively. 
        #for (x,y,w,h) in faces: #uncomment when needing to view the image
        #    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    if (len(faces) != 0):
        closestFace = max(faces, key=lambda x: x[3])

        x = closestFace[0]
        y = closestFace[1]
        w = closestFace[2]
        h = closestFace[3]

        #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2) #uncomment when needing to view the image
        x_mid = 1023 - int(((x + (w/2)) * 1.27875))
        y_mid = 1023 - int(((y + (h/2)) * 1.27875))
        msg = str(x_mid) + ',' + str(y_mid) + '\n'
        msg = msg.encode('ascii')
        ser.write(msg)
        
    #cv2.imshow('frame', frame) #IMPORTANT - uncomment this section to see the frame and wait for 'q' to be pressed to exit
    #if cv2.waitKey(1) & 0xFF == ord('q'): 
    #    break
    
    #manage count variable to not run away
    if count < 20000:
        count += 1
    else:
        count = 0

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
