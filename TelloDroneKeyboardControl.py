from djitellopy import Tello
import cv2

import keyboard


def keyboard_control(tello):
    # STARTING UP THE CAMERA FOR THE TELLO DRONE
    tello.takeoff()
    tello.streamon()
    
        
    # SETTING THE SPEED AND DISTANCE OF THE DRONE
    print("Please use values of \"10 - 100\" for speed and distance and \" -100 - 100\" for turn")
    speed = int(input("Enter the speed of the drone in cm/s\n"))
    distance = int(input("Enter the distance that you would like the drone to travel in centimeters\n"))

    tello.set_speed(speed)

    while True:
        # TELLO CAMERA
        camera = tello.get_frame_read().frame
        camera = cv2.resize(camera, (600, 600))
        cv2.imshow("results", camera)
        cv2.waitKey(1)

        # WASD MOVEMENT
        if(keyboard.is_pressed("w")):
            tello.move_forward(distance)
        if(keyboard.is_pressed("a")):
            tello.move_left(distance)
        if(keyboard.is_pressed("s")):
            tello.move_back(distance)
        if(keyboard.is_pressed("d")):
            tello.move_right(distance)
        
        # CHANGE THE DEGREE THAT THE DRONE IS LOOKING IN
        if(keyboard.is_pressed("q")):
            tello.turn_left(30)
        if(keyboard.is_pressed("e")):
            tello.turn_right(30)

        # ASCEND / DESCEND
        if(keyboard.is_pressed("z")):
            tello.move_down(distance)
        if(keyboard.is_pressed("x")):
            tello.move_up(distance)

        # BUTTON FOR LANDING
        if(keyboard.is_pressed("l")):
            tello.land()
            tello.streamoff()
            break

        # CHANGE THE SPEED AND DISTANCE
        if(keyboard.is_pressed("p")):
            print("Changing the speed and distance settings of the drone")
            print("Please use values of \"10 - 100\" for speed and distance and \" -100 - 100\" for turn")
            speed = int(input("Enter the speed of the drone in cm/s\n"))
            distance = int(input("Enter the distance that you would like the drone to travel in centimeters\n"))
            turn = int(input("Enter the ammount that you would like the drone to turn\n"))
            tello.set_speed(speed)

def flight_test(tello):
    tello.takeoff()

    tello.land()
    

def menu():
    print("1. preform a flight test on the drone")
    print("2. control the tello through keyboard")

    choice = int(input("Choose a number\n"))
    return choice

def main():
    tello = Tello()
    tello.connect()

    battery = tello.get_battery()

    print("battery is ",battery,"%")

    choice = menu()

    if(choice == 1):
        flight_test(tello)
    if(choice == 2):
        keyboard_control(tello)
    
    print("battery is ",battery,"%")

    tello.disconnect()
main()
