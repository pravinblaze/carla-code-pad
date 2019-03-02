import carla

client = carla.Client('localhost', 2000)
world = client.get_world()
map = world.get_map()

initial_waypoint = map.get_waypoint(carla.Location(x=30, y=-8.133))
wp_choice = initial_waypoint.next(10)

for wp in wp_choice:
 wp = wp.next(20)[0]
 print wp.transform.location
