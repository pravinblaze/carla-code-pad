import carla
import random
import time

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()
topology = world_map.get_topology()

lane_list_town04 = [
	carla.Location(-15.4, 140, 5),
	carla.Location(-11.9, 140, 5),
	carla.Location(-8.4, 140, 5),
	carla.Location(-4.9, 140, 5)
]

lane_list_town05 = [
	carla.Location(69.1, 1.9),
	carla.Location(69.1, 5.3),
	carla.Location(99.9, -35.0),
	carla.Location(96.5, -35.0)
]

lane_list_town03 = [
	carla.Location(102.4, -132.5)
]

lane_list_town07_1 = [
	carla.Location(-74.3, -142.0),
	carla.Location(-96.3, -158.2),
	carla.Location(-51.3, -161.8)
]

blueprint = random.choice(world.get_blueprint_library().filter('vehicle.lincoln.mkz2017'))
vehicle_list = []

n = 1
d = 20
lane_list = lane_list_town07_1

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
