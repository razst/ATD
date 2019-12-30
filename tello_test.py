import tello


print("starting...")
my_drone = tello.Tello()
print(my_drone.get_battery())
print(my_drone.get_temp())
my_drone.takeoff()
my_drone.up(60)
my_drone.land()