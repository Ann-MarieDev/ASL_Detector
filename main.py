
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

# Settings 4 media pipe and hand tracking !!!!!!!!! 
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
    
    # This is converting the frames to rgb (open cv uses bgr but mediapipe uses rgb)
    # cvtColor changes the img color in opencv & COLOR_BGR2RGB converts it from blue green red to red green blue
    frame_color_converter = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    #Dectect hands 
    hand_results = hands.process(frame_color_converter)
    
    #If statement: If it sees hands it will show points on the hand (knuckles, wrist, etc)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mediapipe_points.draw_landmarks(frame, hand_landmarks, mediapipe_hands.HAND_CONNECTIONS, mediapipe_points.DrawingSpec(color=(3, 252, 140), thickness=2, circle_radius=2), mediapipe_points.DrawingSpec(color=(212, 255, 236), thickness=2))

    # Displays current frame in a window: Webcam-name of the window
    # imshow is used to create a graphical window and update it with the current frame
    cv.imshow('Webcam', frame)
    
    # Save the current frame as an image by overwriting the same file--no extra memory usage 
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



