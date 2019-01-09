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

destination = -149, 90
while True:
 location = ego_vehicle.get_location()
 origin = location.x, location.y
 plan = grp.plan_route(origin, destination)
 clear()
 print "Route plan to destination"
 for decision in plan:
  print decision
 time.sleep(1)

