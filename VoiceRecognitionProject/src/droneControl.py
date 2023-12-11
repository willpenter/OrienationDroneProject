from djitellopy import Tello
import time

class DroneController:
    def __init__(self):
        self.drone = Tello()

    def connect(self):
        self.drone.connect()
        print(f"Battery: {self.drone.get_battery()}%")

    def takeoff(self):
        self.drone.takeoff()

    def land(self):
        self.drone.land()

    def move_up(self, distance):
        self.drone.move_up(distance)

    def move_down(self, distance):
        self.drone.move_down(distance)

    # Add more methods to control different aspects of the drone

#############################################

def main():
    controller = DroneController()
    controller.connect()

    try:
        controller.takeoff()
        time.sleep(5)
        controller.land()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        controller.drone.end()

if __name__ == "__main__":
    main()