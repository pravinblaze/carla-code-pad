import time
import os
import sys
sys.path.append('/home/praveen/workspace/carla/PythonAPI/agents/navigation/')

import carla

from global_route_planner import GlobalRoutePlanner
from global_route_planner_dao import GlobalRoutePlannerDAO

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

dao = GlobalRoutePlannerDAO(world_map)
grp = GlobalRoutePlanner(dao)
grp.setup()

ego_vehicle = None
possible_vehicles = world.get_actors().filter('vehicle.*')
for vehicle in possible_vehicles:
 if vehicle.attributes['role_name'] == "hero":
  ego_vehicle = vehicle

clear = lambda: os.system('clear')

# destination = -149, 90 # For Town03
destination = 88.5, 30 # For Town01
while True:
 location = ego_vehicle.get_location()
 origin = location.x, location.y
 path = grp.path_search(origin, destination)
 plan = grp.plan_route(origin, destination)
 clear()
 print "Route nodes"
 print path
 print "Route plan to destination"
 for decision in plan:
  print decision
 time.sleep(1)

