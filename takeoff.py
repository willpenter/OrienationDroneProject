from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(50)
tello.rotate_clockwise(50)
tello.move_forward(50)

tello.land()
