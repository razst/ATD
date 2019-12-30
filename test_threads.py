import tello
import time
my_drone = tello.Tello()
print("start")
print(my_drone.get_battery())
print(my_drone.get_temp())
my_drone.streamon()
'''
my_drone.takeoff()
my_drone.up(40)
my_drone.back(30)
my_drone.forward(30)
time.sleep(120)
my_drone.land()
'''
time.sleep(120)
my_drone.streamoff()
print(my_drone.get_temp())