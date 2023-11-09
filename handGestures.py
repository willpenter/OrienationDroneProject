import cv2
import mediapipe as mp
from djitellopy import Tello


# Initialize Mediapipe hands module
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)


# Initialize Tello drone
tello = Tello()
tello.connect()
tello.streamon()  # Start video stream
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)


# Initialize OpenCV video capture for PC camera
pc_camera_cap = cv2.VideoCapture(0)


# Initialize OpenCV video capture for Tello stream
tello_camera_cap = cv2.VideoCapture('udp://0.0.0.0:11111')
width = 300
height = 280
tello_camera_cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
tello_camera_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# Direction mapping
direction_mapping = {
    "Right": "right",
    "Left": "left",
    "Forward": "forward",
    "Backward": "backward",
    "Up": "up",
    "Down": "down",
}


while True:
    # Read frame from PC camera
    ret_pc_camera, pc_camera_frame = pc_camera_cap.read()


    # Read frame from Tello camera
    ret_tello_camera, tello_camera_frame = tello_camera_cap.read()


    if ret_pc_camera and ret_tello_camera:
        # Convert the PC camera frame to RGB for Mediapipe
        pc_camera_frame_rgb = cv2.cvtColor(pc_camera_frame, cv2.COLOR_BGR2RGB)


        # Process the PC camera frame with Mediapipe hands
        results = hands.process(pc_camera_frame_rgb)


        # Initialize direction as "No Direction"
        direction = "No Direction"


        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the landmarks for the hand
                thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                index_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y


                horizontal_diff = thumb_x - index_x
                vertical_diff = thumb_y - (index_y + middle_y) / 2
                avg_y = (index_y + middle_y) / 2


                #  Directions
                # Up
                if vertical_diff < -0.1:
                    direction = "Up"
                    tello.send_rc_control(0, 0, 15, 0)
                #  Down
                elif vertical_diff > 0.1:
                    direction = "Down"
                    tello.send_rc_control(0, 0, -15, 0)
                # RIght
                elif horizontal_diff > 0.1:
                    direction = "Right"
                    tello.send_rc_control(15, 0, 0, 0)
                # Left
                elif horizontal_diff < -0.1:
                    direction = "Left"
                    tello.send_rc_control(-15, 0, 0, 0)
                # Forward
                elif index_y < avg_y - 0.1:
                    direction = "Forward"
                    tello.send_rc_control(0, 15, 0, 0)
                # Backward
                elif index_y > avg_y + 0.1:
                    direction = "Backward"
                    tello.send_rc_control(0, -15, 0, 0)            
                # Rotate
                else:
                    direction = "No Direction"
                    tello.send_rc_control(0, 0, 0, 0)


                # Draw landmarks on the PC camera frame
                mp_drawing.draw_landmarks(pc_camera_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())


        # Display the PC camera frame with direction and landmarks
        cv2.putText(pc_camera_frame, f"Direction: {direction_mapping.get(direction, 'No Direction')}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Hand Gestures (PC Camera)", pc_camera_frame)


        # Display the Tello camera frame
        cv2.imshow("Tello Camera", tello_camera_frame)


    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release resources
tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()  # Stop video stream
tello.disconnect()
pc_camera_cap.release()
tello_camera_cap.release()
cv2.destroyAllWindows()