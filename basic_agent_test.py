# Hell yeah !

import os
import random
import sys

import numpy as np
import carla
from carla import ColorConverter as cc
import pygame

sys.path.append(os.path.abspath('/home/praveen/workspace/carla/PythonAPI/agents/navigation/'))
from basic_agent import BasicAgent
from global_route_planner import GlobalRoutePlanner
from global_route_planner_dao import GlobalRoutePlannerDAO

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

vehicle = None
camera_sensor = None
class surface_holder:
    def __init__(self):
        self.surface = None
camera_holder = surface_holder()

try:

	###############################################################################################################
	dao = GlobalRoutePlannerDAO(world_map)
	grp = GlobalRoutePlanner(dao)
	grp.setup()

	# Obtain route plan
	# route = grp.plan_route((43.70042037963867, # -7.828187465667725), (44.610050201416016, -192.88201904296875))

	route = grp.plan_route((43.70014190673828, -7.828191757202148), (44.610050201416016, -192.88201904296875))
	print(route)
	###############################################################################################################

	# Spawn vehicle

	blueprint = random.choice(
	world.get_blueprint_library().filter('vehicle.tesla.model3'))
	blueprint.set_attribute('role_name', 'hero')
	if blueprint.has_attribute('color'):
		color = random.choice(blueprint.get_attribute('color').recommended_values)
		blueprint.set_attribute('color', color)

	while vehicle is None:
		# spawn_points = world.get_map().get_spawn_points()
		# spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
		spawn_point = carla.Transform(carla.Location(x = 43.7, y = -7.8), carla.Rotation(yaw = 180))
		vehicle = world.try_spawn_actor(blueprint, spawn_point)

	agent = BasicAgent(vehicle)
	agent.set_destination((44.61, -192.88, 0))

	# Set sensor

	bp_library = world.get_blueprint_library()
	bp = bp_library.find('sensor.camera.rgb')
	bp.set_attribute('image_size_x', str(1920/2))
	bp.set_attribute('image_size_y', str(1080/2))

	camera_transform = carla.Transform(
	carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15))
	camera_sensor = world.spawn_actor(
	bp,
	camera_transform,
	attach_to=vehicle)

	# Camera callback funtion

	def parse_image(image):
		image.convert(cc.Raw)
		array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
		array = np.reshape(array, (image.height, image.width, 4))
		array = array[:, :, :3]
		array = array[:, :, ::-1]
		surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
		camera_holder.surface = surface

	camera_sensor.listen(lambda image: parse_image(image))

	# Project camera image on pygame
	display = pygame.display.set_mode(
	(1920/2, 1080/2),
	pygame.HWSURFACE | pygame.DOUBLEBUF)

	# Game loop
	clock = pygame.time.Clock()

	while True:
		control = agent.run_step()
		vehicle.apply_control(control)
		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
			sys.exit()
		clock.tick_busy_loop(60)
		while camera_holder.surface is None:
		    # print 'waiting for surface'
		    pass
		display.blit(camera_holder.surface, (0, 0))
		pygame.display.flip()

finally:
	if vehicle is not None:
		vehicle.destroy()
	if camera_sensor is not None:
		camera_sensor.destroy()

