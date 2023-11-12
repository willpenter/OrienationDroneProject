import keyboard
from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager

api_key = "ENTER YOUR API KEY HERE"

with DroneBlocksSimulatorContextManager(simulator_key = api_key) as tello:
    tello.takeoff()
    speed = int(input("Set the speed of the drone\n"))
    distance = int(input("Set the distance of the drone\n"))
    tello.set_speed(speed)
    while True:
         while True:
            # WASD MOVEMENT
            if(keyboard.is_pressed("w")):
                tello.fly_forward(distance, "in")
            if(keyboard.is_pressed("a")):
                tello.fly_left(distance, "in")
            if(keyboard.is_pressed("s")):
                tello.fly_back(distance, "in")
            if(keyboard.is_pressed("d")):
                tello.fly_right(distance, "in")
            # CHANGE THE DEGREE THAT THE DRONE IS LOOKING cm
            if(keyboard.is_pressed("q")):
                tello.yaw_left(30)
            if(keyboard.is_pressed("e")):
                tello.yaw_right(30)
            # ASCEND / DESCEND
            if(keyboard.is_pressed("z")):
                tello.fly_up(distance, "in")
            if(keyboard.is_pressed("x")):
                tello.fly_down(distance, "in")
            # BUTTON FOR LANDING
            if(keyboard.is_pressed("l")):
                tello.land()
                break
            # Changing THE SPEED AND DISTANCE OF THE DRONE
            if(keyboard.is_pressed("r")):
                speed = int(input("Set the speed of the drone\n"))
                distance = int(input("Set the distance of the drone"))
                tello.set_speed(speed)