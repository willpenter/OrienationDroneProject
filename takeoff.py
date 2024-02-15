from djitellopy import Tello
#This code just takes off and lands, usable for flight test
tello = Tello()

tello.connect()
tello.takeoff()


tello.land()
