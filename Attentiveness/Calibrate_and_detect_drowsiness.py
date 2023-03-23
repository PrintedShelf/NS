from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import os
import cv2
import time

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor(os.getcwd() +"/data/shape_predictor_68_face_landmarks.dat")

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def detect_drowsiness(thresh):
     threshold = thresh - 0.07
     frame_check = 20
     (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
     (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

     cap=cv2.VideoCapture(0)
     flag=0
     attn=1
     while True:
        GAZE = 'Face not detected'

        ret, img=cap.read()
        img = imutils.resize(img, width=450)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        txt='Not Attentive'
        for subject in subjects:
            structure = predict(gray, subject)
            structure = face_utils.shape_to_np(structure)
            if subjects != []:
                for subject in subjects:
                    x = subject.left()
                    y = subject.top()
                    w = subject.right() - x
                    h = subject.bottom() - y
                    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    txt = 'Attentive'
                    GAZE = ''

            leftEye = structure[lStart:lEnd]
            rightEye = structure[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(img, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(img, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < threshold:
                flag += 1
                if flag >= frame_check:
                    cv2.putText(img, "********DROWSINESS DETECTED!**********", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    txt='Not Attentive'
            else:
                flag = 0
        cv2.putText(img, GAZE, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(img, txt, (10, 325),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Frame",img)
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break
     cv2.destroyAllWindows()
     cap.release() 

def calibrate():
     thresh = []
     detect = dlib.get_frontal_face_detector()
     predict = dlib.shape_predictor('/Users/printedshelf/Desktop/Attentiveness/NS/Attentiveness/data/shape_predictor_68_face_landmarks.dat')
     (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
     (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

     cap=cv2.VideoCapture(0)
     flag=0
     attn=1
     capture_duration = 5
     start_time = time.time()
     while( int(time.time() - start_time) < capture_duration ):
        ret, img=cap.read()
        img = imutils.resize(img, width=450)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        for subject in subjects:
            structure = predict(gray, subject)
            structure = face_utils.shape_to_np(structure)
            if subjects != []:
                for subject in subjects:
                    x = subject.left()
                    y = subject.top()
                    w = subject.right() - x
                    h = subject.bottom() - y
                    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    txt = 'Attentive'
                    GAZE = ''

            leftEye = structure[lStart:lEnd]
            rightEye = structure[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(img, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(img, [rightEyeHull], -1, (0, 255, 0), 1)
            thresh.append(ear)
            cv2.putText(img, "Calibrating!!!!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Frame",img)
        key = cv2.waitKey(10) & 0xFF  
     cv2.destroyAllWindows()
     cap.release()
     if len(thresh):
         return sum(thresh)/len(thresh)
     else:
         return 0
     
get_thresh = calibrate()
if get_thresh:
    detect_drowsiness(get_thresh)
else:
    print('Try recalibrating!!!')