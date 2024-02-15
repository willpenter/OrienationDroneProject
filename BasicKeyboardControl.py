# This is a basic way of controlling the DJI Tello using the Computer Keyboard, change it how you like
from djitellopy import Tello
import cv2
import threading
import keyboard

def keyboard_control(tello):
    tello.takeoff()

    speed = 20  # Set speed to 20 cm/s
    distance = 20  # Set distance to 20 cm
    tello.set_speed(speed)

    def key_handler():
        while True:
            if keyboard.is_pressed('w'):
                tello.move_forward(distance)
            elif keyboard.is_pressed('a'):
                tello.move_left(distance)
            elif keyboard.is_pressed('s'):
                tello.move_back(distance)
            elif keyboard.is_pressed('d'):
                tello.move_right(distance)
            elif keyboard.is_pressed('q'):
                tello.rotate_counter_clockwise(30)
            elif keyboard.is_pressed('e'):
                tello.rotate_clockwise(30)
            elif keyboard.is_pressed('z'):
                tello.move_down(distance)
            elif keyboard.is_pressed('x'):
                tello.move_up(distance)
            elif keyboard.is_pressed('l'):
                tello.land()
                tello.streamoff()
                break
            elif keyboard.is_pressed('p'):
                print("Speed and distance are already set to 20 cm/s and 20 cm.")

    key_thread = threading.Thread(target=key_handler)
    key_thread.start()

    while True:
        camera = tello.get_frame_read().frame
        camera = cv2.resize(camera, (600, 600))
        cv2.imshow("Tello Camera", camera)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    key_thread.join()

def flight_test(tello):
    tello.takeoff()
    # Add your flight test actions here
    
    tello.land()

def main():
    tello = Tello()
    tello.connect()
    battery = tello.get_battery()
    print("Battery is:", battery, "%")

    choice = int(input("Choose an option:\n1. Perform a flight test\n2. Control the Tello through keyboard\n"))

    if choice == 1:
        flight_test(tello)
    elif choice == 2:
        keyboard_control(tello)

    tello.disconnect()
    print("Battery is:", battery, "%")

if __name__ == "__main__":
    main()
