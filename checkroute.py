import os
import sys
import random
import time

import carla

sys.path.append(os.path.abspath('/home/praveen/workspace/carla/PythonAPI/agents/navigation/'))
from basic_agent import BasicAgent

from global_route_planner import GlobalRoutePlanner
from global_route_planner_dao import GlobalRoutePlannerDAO

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

dao = GlobalRoutePlannerDAO(world_map)
grp = GlobalRoutePlanner(dao)
grp.setup()

# Obtain route plan
# route = grp.plan_route((43.70042037963867, # -7.828187465667725), (44.610050201416016, -192.88201904296875))

route = grp.plan_route((43.70014190673828, -7.828191757202148), (44.610050201416016, -192.88201904296875))
print(route)

blueprint = world.get_blueprint_library().find('vehicle.lincoln.mkz2017')
blueprint.set_attribute('role_name', 'hero')

spawn_point = carla.Transform(carla.Location(x = 43.7, y = -7.8), carla.Rotation(yaw = 180))
vehicle = world.try_spawn_actor(blueprint, spawn_point)

agent = BasicAgent(vehicle)
agent.set_destination((44.61, -192.88, 0))


while True:
	control = agent.run_step()
	vehicle.apply_control(control)
	time.sleep(0.06)

