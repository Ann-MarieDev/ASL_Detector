
#------------------------------------Imports------------------------------------
#Import mediapipe pkg into project
import mediapipe as mp

#Import cv2: Aka acssesing the camera
import cv2 as cv

#Import the vision tasks: Aka video and image input
from mediapipe.tasks.python import vision 

#Import functions/unit tests/logging stuff if broken

#Import asl signs data to translate signs
#import asl_signs as hand_data
from utils import asl_signs

#------------------------------------Mediapipe setup------------------------------------
#Variable that acesses mediaspipes stuff
mediapipe_hands = mp.solutions.hands

# Settings 4 media pipe and hand tracking !!!!!!!!! 😒 this is so confusing 
hands = mediapipe_hands.Hands(
    static_image_mode = False,    # False means we're working with video, not "static" images
    max_num_hands = 2,            # Detect up to 2 hands in the frame
    min_detection_confidence = 0.4,# How sure MediaPipe needs to be that it sees a hand (70%)
    min_tracking_confidence = 0.2  # How sure it needs to be to keep tracking a hand (50%)
)

#Variable so we can see the hand points (knuckles, wrist, etc etc)
mediapipe_points = mp.solutions.drawing_utils


#------------------------------------Acssesing the camera------------------------------------
#Opens the webcam: This makes a object "capture" that lets you control and retrieve frames from the webcam
#Default webcam: 0
capture = cv.VideoCapture(0)

#While true: Starts an infinite loop to process each frame
while True:
    #Reads 1 frame from the webcam; isTrue: Tells if it was correctly captured; frame data (1 frame)
    isTrue, frame = capture.read()
    
    #Tells me if it could not read the webcam/it failed
    if not isTrue:
        print("Could not read frame in video/webcam")
        break
    
    # For some reason mediapipe needs rgb? So this is converting the frames to rgb (open cv uses bgr but mediapipe uses rgb.. bruhh what)
    # cvtColor changes the img color in opencv & COLOR_BGR2RGB converts it from blue green red to red green blue
    frame_color_converter = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    #Dectect hands 
    hand_results = hands.process(frame_color_converter)
    
    #If statement: If it sees hands it will show points on the hand (knuckles, wrist, etc)
    
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mediapipe_points.draw_landmarks(frame, hand_landmarks, mediapipe_hands.HAND_CONNECTIONS, mediapipe_points.DrawingSpec(color=(199,21,133), thickness=2, circle_radius=2), mediapipe_points.DrawingSpec(color=(195, 177, 225), thickness=2))

    #Displays current frame in a window: Webcam-name of the window
    #"imshow is used to create a graphical window and update it with the current frame" whateva that means
    cv.imshow('Webcam', frame)
    
    # Save the current frame as an image by overwriting the same file--no extra memory usage 😛... y the emoji sideways
    cv.imwrite('current_frame.jpg', frame)
    
    #cv2.waitKey(1) waits for 1 millisecond for a key press; 
    #& 0xFF compatibility from systems when interpreting key presses;
    #ord('q') is the ascii value of the letter 'q' if you press q the loop breaks
    if cv.waitKey(1) & 0xFF == ord('q'): # q for quit
        break
#------------------------------------Clean-up------------------------------------
#Stops the webcam from being used by program (releases the webcam hint hint)
#If I dont add this it could prevent other things from using the webcam
capture.release()

#Closes all the windows
cv.destroyAllWindows()






'''
Leanring basics
#------------------------------------Acssesing the camera------------------------------------
#Reminder: You can set the argument to 0 for webcam/or file path for video
capture = cv.VideoCapture('media/videos/hi.mp4')
''
This while statement returns if it read the frames in the webcam/video.
EX: 
capture.read(): Reads every frame in the video
isTrue: Returns if the frame was correctly read
frame: Returns the frame (this is the frame data---a image represented as a NumPy array)
----------
cv.waitKey(20) pauses for 20 milliseconds between frames--video playback speed
''
while True:
    #Reads and returns every frame (reads sequential frames until the video ends or the loop is broken)
    isTrue, frame = capture.read()
    
    #Displays the frame
    cv.imshow('media', frame)
    
    #Add a ending to the video/webcam time or it will play/go infinatly 
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
  
#Displays the video/destorys the window once done playing  
capture.release()
cv.destroyAllWindows()
'''
'''
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands model
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the output
        cv2.imshow("Webcam - ASL Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release webcam and close all windows
cap.release()
cv2.destroyAllWindows()
'''