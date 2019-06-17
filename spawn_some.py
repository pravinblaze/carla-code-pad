import carla
import random
import time

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()
topology = world_map.get_topology()

lane_list = [
	carla.Location(-15.4, 140, 5),
	carla.Location(-11.9, 140, 5),
	carla.Location(-8.4, 140, 5),
	carla.Location(-4.9, 140, 5)
]

blueprint = random.choice(world.get_blueprint_library().filter('vehicle.lincoln.mkz2017'))
vehicle_list = []
n = 25
d = 15

try:
	for lane in lane_list:
		wp = world_map.get_waypoint(lane)
		for _ in range(n):
			vehicle = world.try_spawn_actor(blueprint, wp.transform)
			vehicle_list.append(vehicle)
			wp = wp.next(d)[0]
	
	while True:
		time.sleep(1)

finally:
	
	for vehicle in vehicle_list:
		vehicle.destroy()
