import cv2
import mediapipe as mp
import math
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.streamon()  # Start video stream
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)
# Initialize MediaPipe Hands model
hands = mp.solutions.hands.Hands(max_num_hands=1)
pose = mp.solutions.pose.Pose()
side = 0
last_side = 0

# Function to detect hand gestures
def detect_gestures(frame):
    global side
    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results_hands = hands.process(rgb_frame)
    results_pose = pose.process(rgb_frame)

    # hand image processing
    if results_hands.multi_hand_landmarks and results_pose.pose_landmarks:

        for hand_landmarks in results_hands.multi_hand_landmarks:
            #index finger tip
            index_finger_landmark = hand_landmarks.landmark[8]
            index_x = int(index_finger_landmark.x * frame.shape[1])
            index_y = int(index_finger_landmark.y * frame.shape[0])
            cv2.circle(frame, (index_x, index_y), 5, (255, 0, 0), -1)

            #thumb tip
            thumb_finger_landmark = hand_landmarks.landmark[4]
            thumb_x = int(thumb_finger_landmark.x * frame.shape[1])
            thumb_y = int(thumb_finger_landmark.y * frame.shape[0])
            cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 255, 0), -1)
            
            #thumb bottom
            thumb_finger_bottom_landmark = hand_landmarks.landmark[1]
            thumb_bottom_x = int(thumb_finger_bottom_landmark.x * frame.shape[1])
            thumb_bottom_y = int(thumb_finger_bottom_landmark.y * frame.shape[0])
            cv2.circle(frame, (thumb_bottom_x, thumb_bottom_y), 5, (255, 0, 0), -1)

            #palm
            palm_landmark = hand_landmarks.landmark[0]
            palm_x = int(palm_landmark.x * frame.shape[1])
            palm_y = int(palm_landmark.y * frame.shape[0])
            cv2.circle(frame, (palm_x, palm_y), 5, (0, 150, 150), -1)

            #middle finger tip
            middle_finger_landmark = hand_landmarks.landmark[12]
            middle_x = int(middle_finger_landmark.x * frame.shape[1])
            middle_y = int(middle_finger_landmark.y * frame.shape[0])
            cv2.circle(frame, (middle_x, middle_y), 5, (255, 0, 0), -1)

            #ring finger tip
            ring_finger_landmark = hand_landmarks.landmark[16]
            ring_x = int(ring_finger_landmark.x * frame.shape[1])
            ring_y = int(ring_finger_landmark.y * frame.shape[0])
            cv2.circle(frame, (ring_x, ring_y), 5, (255, 0, 0), -1)

            #pinky finger tip
            pinky_finger_landmark = hand_landmarks.landmark[20]
            pinky_x = int(pinky_finger_landmark.x * frame.shape[1])
            pinky_y = int(pinky_finger_landmark.y * frame.shape[0])
            cv2.circle(frame, (pinky_x, pinky_y), 5, (255, 0, 0), -1)

            cv2.line(frame, (index_x, index_y), (thumb_x, thumb_y), (0, 0, 255), thickness=2)
            cv2.line(frame, (index_x, index_y), (thumb_bottom_x, thumb_bottom_y), (0, 0, 255), thickness=2)
            cv2.line(frame, (thumb_bottom_x, thumb_bottom_y), (thumb_x, thumb_y), (0, 0, 255), thickness=2)


        #pose image processing
        right_shoulder_landmark = results_pose.pose_landmarks.landmark[12]
        right_shoulder_x = int(right_shoulder_landmark.x * frame.shape[1])
        right_shoulder_y = int(right_shoulder_landmark.y * frame.shape[0])
        cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 5, (255, 0, 0), -1)

        left_shoulder = results_pose.pose_landmarks.landmark[11]
        left_shoulder_x = int(left_shoulder.x * frame.shape[1])
        left_shoulder_y = int(left_shoulder.y * frame.shape[0])
        cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 5, (255, 0, 0), -1)


        # gesture detection only occurs when hands are above shoulder
        if(right_shoulder_landmark.y > palm_landmark.y):

            #open-closed detection
            if(angle_between_lines((thumb_bottom_x, thumb_bottom_y, thumb_x, thumb_y), (thumb_bottom_x, thumb_bottom_y, index_x, index_y)) > 30):
                position = "open"
            else:
                position = "closed"
            frame = cv2.putText(frame, position, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            #coyote detection

            #if(math.sqrt((ring_finger_landmark.x - middle_finger_landmark.x)**2 + (ring_finger_landmark.y - middle_finger_landmark.y)**2) < .2 and 
            #math.sqrt((index_finger_landmark.x - pinky_finger_landmark.x)**2 + (index_finger_landmark.y - pinky_finger_landmark.y)**2) > .2):
            #    position = "coyote"
            #else:
            #    position = "none"
            #frame = cv2.putText(frame, position, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            #side hand is on of frame
            if(palm_landmark.x > 0.5):
                side = 1
            else:
                side = 2

    return frame

def angle_between_lines(line1, line2):
    # Extract endpoints of the lines
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Calculate vectors along the lines
    vector1 = (x2 - x1, y2 - y1)
    vector2 = (x4 - x3, y4 - y3)

    # Calculate dot product and magnitude of vectors
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    # Calculate cosine of the angle between the vectors
    cosine_angle = dot_product / (magnitude1 * magnitude2)

    # Convert cosine angle to radians and then to degrees
    angle = math.acos(cosine_angle)
    angle_degrees = math.degrees(angle)

    return angle_degrees

# Capture video from webcam
cap = cv2.VideoCapture('udp://0.0.0.0:11111')

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    # Detect gestures
    frame = detect_gestures(frame)

    # Display the resulting frame
    cv2.imshow('Hand Gestures', frame)
 
    if(side != last_side):
        print(f'side: {side}')
        last_side = side

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# Release the capture


tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()  # Stop video stream
tello.disconnect()
cap.release()
cv2.destroyAllWindows()