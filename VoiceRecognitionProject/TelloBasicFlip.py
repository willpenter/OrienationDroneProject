from djitellopy import Tello
import time

# Connect to the Tello drone
tello = Tello()
tello.connect()

# Take off
tello.takeoff()
time.sleep(2)

# Perform a flip (you can change the direction if needed)
tello.flip("f")  # "l" for left, "r" for right, "f" for forward, "b" for backward
time.sleep(2)

# Land
tello.land()

# Disconnect from the Tello drone
tello.end()
