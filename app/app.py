from tensorflow.keras.models import load_model
import mediapipe as mp
import cv2
from threading import Thread
import numpy as np
import playsound
import requests as req

# ---Import trained CNN model---
model = load_model('./model.h5')
print(model.summary())

# ---Import landmark detection model---
# initialize mediapipe's facemesh landmark detector
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.3, min_tracking_confidence=0.8)

# import tools to draw mesh over face
mp_drawing = mp.solutions.drawing_utils 
drawing_spec = mp_drawing.DrawingSpec(color=(0, 230, 0), thickness=1, circle_radius=1)

# ---Initialize constants---
# mediapipe facemesh landmark coordinates for eyes and mouth 
right_eye_coordinates = [[33, 133], [160, 144], [159, 145], [158, 153]]
left_eye_coordinates = [[263, 362], [387, 373], [386, 374], [385, 380]]
mouth_coordinates = [[61, 291], [39, 181], [0, 17], [269, 405]]

# Base url of web api that receives requests and updates the database when an alarm or a yawn is detected
BASE_URL = 'https://sleepywheels.vercel.app'

# color for drawing on video frame
COLOR = (0, 160, 0)

# CNN input dimension: length of each side of square image (1 video frame) feeded into the CNN model as input
CNN_INPUT_DIM = 224
# threshold number of drowsy frames; if cnn_frame_counter >= CNN_CONSEC_FRAMES, driver must be alerted using the alarm
CNN_CONSEC_FRAMES = 15

# if eye aspect ratio falls below EYE_AR_THRESH, a blink is detected 
EYE_AR_THRESH = 0.26
# if eye_frame_counter >= EYE_AR_CONSEC_FRAMES, drowsy behaviour is detected and alarm is sounded
EYE_AR_CONSEC_FRAMES = 15

# if mouth aspect ratio is above MOUTH_AR_THRESH, the system concludes that current frame contains a mouth open wide enough that it could be part of a series of frames constituting a yawn
MOUTH_AR_THRESH = 0.05
# if mouth_frame_counter >= MOUTH_AR_CONSEC_FRAMES, a yawn is recorded
MOUTH_AR_CONSEC_FRAMES = 20

# ---Initialize global variables---
# a boolean to keep track of whether the alarm is currently ringing or not
is_alarm_on = False

# counts number of consecutive frames in which the CNN has detected sleepy behaviour
cnn_frame_counter = 0

# counts number of consecutive frames during which eye aspect ratio is above threshold
eye_frame_counter = 0

# counts number of consecutive frames during which mouth aspect ratio is above threshold
mouth_frame_counter = 0

# counts number of yawns recorded
yawn_counter = 0

# ---Utility functions---
def distance(point1, point2):
    return (((point1[:2] - point2[:2])**2).sum())**0.5

def record_alarm():
    url = BASE_URL + '/alarm'

    # try:
    #     resp = req.post(url, timeout=5)
    #     if resp != None:
    #         print('Alarm recorded')
    # except:
    #     print('[ERROR] Error during network request made to record alarm')
    #     return
        
def record_yawn():
    url = BASE_URL + '/yawn'

    # try:
    #     resp = req.post(url, timeout=5)
    #     if resp != None:
    #         print('Yawn recorded')
    # except:
    #     print('[ERROR] Error during network request made to record yawn')
    #     return
        
def sound_alarm(path):
    playsound.playsound(path)
    record_alarm()
    
# returns True if CNN classifies video frame as sleepy
def is_frame_sleepy_according_to_cnn(cnn_input_img):
    model_output = model.predict(cnn_input_img.reshape(-1, CNN_INPUT_DIM, CNN_INPUT_DIM, 3))
    # model_output[0][0] == 1 => driver is sleepy
    # model_output[0][1] == 1 => driver is alert
    return model_output[0][0] == 1

def calc_eye_aspect_ratio(landmarks, eye):
    N1 = distance(landmarks[eye[1][0]], landmarks[eye[1][1]])
    N2 = distance(landmarks[eye[2][0]], landmarks[eye[2][1]])
    N3 = distance(landmarks[eye[3][0]], landmarks[eye[3][1]])
    D = distance(landmarks[eye[0][0]], landmarks[eye[0][1]])
    ear = (N1 + N2 + N3) / (3 * D)
    return ear

def calc_mouth_aspect_ratio(landmarks):
    N1 = distance(landmarks[mouth_coordinates[1][0]], landmarks[mouth_coordinates[1][1]])
    N2 = distance(landmarks[mouth_coordinates[2][0]], landmarks[mouth_coordinates[2][1]])
    N3 = distance(landmarks[mouth_coordinates[3][0]], landmarks[mouth_coordinates[3][1]])
    D = distance(landmarks[mouth_coordinates[0][0]], landmarks[mouth_coordinates[0][1]])
    mar = (N1 + N2 + N3)/(3*D)
    return mar

def draw_face_mesh(frame, results):
    for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)

# returns True if alarm must be sounded according to CNN
def cnn_check(frame):
    global cnn_frame_counter
    is_sleepy_via_cnn = False
    cnn_input_img = cv2.resize(frame, (CNN_INPUT_DIM, CNN_INPUT_DIM), interpolation = cv2.INTER_AREA)
    
    if is_frame_sleepy_according_to_cnn(cnn_input_img):
        cnn_frame_counter += 1
        cv2.putText(frame, "CNN (current frame): Sleepy", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)
    else:
        cnn_frame_counter = 0
        cv2.putText(frame, "CNN (current frame): Alert", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)
    
    if cnn_frame_counter >= CNN_CONSEC_FRAMES:
        is_sleepy_via_cnn = True

    return is_sleepy_via_cnn

# returns True if alarm must be sounded according to Landmark Detector
def landmark_detector_check(frame):
    global is_alarm_on, eye_frame_counter, mouth_frame_counter, yawn_counter
    is_sleepy_via_ear = False

    face_mesh_input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    results = face_mesh.process(face_mesh_input_img)
    
    if results.multi_face_landmarks:
        landmarks_positions = []

        # assume that only face is present in the image
        for _, data_point in enumerate(results.multi_face_landmarks[0].landmark):
            landmarks_positions.append([data_point.x, data_point.y, data_point.z]) # saving normalized landmark positions
        landmarks_positions = np.array(landmarks_positions)
        landmarks_positions[:, 0] *= frame.shape[1]
        landmarks_positions[:, 1] *= frame.shape[0]
        
        # draw face mesh over image
        draw_face_mesh(frame, results)

        # compute the eye aspect ratio for both eyes
        left_ear = calc_eye_aspect_ratio(landmarks_positions, left_eye_coordinates)
        right_ear = calc_eye_aspect_ratio(landmarks_positions, right_eye_coordinates)
        # average out the eye aspect ratio over both eyes
        ear = (left_ear + right_ear) / 2.0
        
        # find mouth aspect ratio
        mar = calc_mouth_aspect_ratio(landmarks_positions)
        
        
        # ---EAR ops---
        # draw the computed eye aspect ratio on the frame to help with debugging and setting the correct eye aspect ratio thresholds and sleepy frame counters
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)

        # check to see if the eye aspect ratio is below the blink threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            eye_frame_counter += 1
        # otherwise, the eye aspect ratio is not below the blink threshold, so reset the counter and alarm
        else:
            eye_frame_counter = 0
            is_alarm_on = False
        
        # if the eyes were closed for a sufficient number of consecutive frames, mark the ear boolean to True to sound the alarm
        if eye_frame_counter >= EYE_AR_CONSEC_FRAMES:
            is_sleepy_via_ear = True
        
        
        # ---MAR ops---
        # draw the computed mouth aspect ratio on the frame to help with debugging and setting the correct mouth aspect ratio thresholds and yawn frame counters
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)
        
        # display number of yawns recorded
        cv2.putText(frame, "Yawns recorded: " + str(yawn_counter), (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)

        # check to see if the mouth aspect ratio is above the yawn threshold, and if so, increment the yawn frame counter
        if mar > MOUTH_AR_THRESH:
            mouth_frame_counter += 1
            # if the mouth was wide open for a sufficient number of frames then sound the alarm
            if mouth_frame_counter == MOUTH_AR_CONSEC_FRAMES:
                # draw a yawn notification on the frame
                yawn_counter += 1
                cv2.putText(frame, "Yawn recorded!", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)
                record_yawn()
        # otherwise, the mouth aspect ratio is not above the yawn threshold, so reset the counter
        else:
            mouth_frame_counter = 0
    
    return is_sleepy_via_ear

# ---Drowsiness detection---
print("[INFO] Starting video stream thread...")

# Webcam
# cap = cv2.VideoCapture(0)

# Video file
video_file_path = '/home/user/Videos/video.mp4'
capture = cv2.VideoCapture(video_file_path)

if not capture.isOpened:
    print('[ERROR] Failed to open video capture')
    exit()

# loop over frames from the video stream
while True:
    _, frame = capture.read()
    if frame is None:
        print('[ERROR] Failed to capture valid video frame')
        break
    
    is_sleepy_via_cnn = cnn_check(frame)
    is_sleepy_via_ear = landmark_detector_check(frame)

    cv2.putText(frame, f"According to CNN: {'Sleepy' if is_sleepy_via_cnn else 'Alert'}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)
    cv2.putText(frame, f"According to EAR: {'Sleepy' if is_sleepy_via_ear else 'Alert'}", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2)

    if is_sleepy_via_cnn or is_sleepy_via_ear:
        # if the alarm is not on, turn it on
        if not is_alarm_on:
            is_alarm_on = True
            t = Thread(target=sound_alarm, args=("./alarm.wav",))
            t.deamon = True
            t.start()
        
        # draw a Wake Up sign on the frame
        cv2.putText(frame, "Wake Up!", (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2)
    
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# --cleanup--
capture.release()
cv2.destroyAllWindows()
