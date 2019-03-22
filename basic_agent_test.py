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

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

vehicle = None
camera_sensor = None
class surface_holder:
    def __init__(self):
        self.surface = None
camera_holder = surface_holder()

try:

	# Spawn vehicle

	blueprint = random.choice(
	world.get_blueprint_library().filter('vehicle.tesla.model3'))
	blueprint.set_attribute('role_name', 'hero')
	if blueprint.has_attribute('color'):
		color = random.choice(blueprint.get_attribute('color').recommended_values)
		blueprint.set_attribute('color', color)

	while vehicle is None:
		# <Town01>
		# spawn_point = carla.Transform(carla.Location(x = 249.18, y = -2.25, z = 1), carla.Rotation(yaw = 180)) # 1
		spawn_point = carla.Transform(carla.Location(338.70, 226.75, 0.00), carla.Rotation(yaw=270)) # 2
		# <Town02>
		# spawn_point = carla.Transform(carla.Location(x = 165.34, y = 188.116, z = 1), carla.Rotation(yaw = 180)) # 1
		# <Town03> Segmentation fault, cannot test !
		# spawn_point = carla.Transform(carla.Location(x = 165.34, y = 188.116, z = 1), carla.Rotation(yaw = 180)) # 1
		# <Town04>
		# spawn_point = carla.Transform(carla.Location(x = -200, y = 37, z = 5), carla.Rotation(yaw = 0)) # 1
		# spawn_point = carla.Transform(carla.Location(x = 381.5, y = -121.2, z = 1), carla.Rotation(yaw = 90)) # 2
		# spawn_point = carla.Transform(carla.Location(x = 176.1, y = -375, z = 1), carla.Rotation(yaw = 0)) # 3
		# spawn_point = carla.Transform(carla.Location(x = 227.6, y = -374.7, z = 1), carla.Rotation(yaw = 0)) # 4
		# <Town05>
		# spawn_point = carla.Transform(carla.Location(x = -54.75, y = -53, z = 1), carla.Rotation(yaw = 90)) # 1
		# spawn_point = carla.Transform(carla.Location(x = -124.4, y = -111.9, z = 1), carla.Rotation(yaw = 90)) # 2
		# spawn_point = carla.Transform(carla.Location(x = -124.4, y = -111.9, z = 1), carla.Rotation(yaw = 270)) # 3
		# spawn_point = carla.Transform(carla.Location(x = 196.86, y = -1.7, z = 1), carla.Rotation(yaw = 90)) # 4
		# <Town06>
		# spawn_point = carla.Transform(carla.Location(x = 196.86, y = -1.7, z = 1), carla.Rotation(yaw = 90)) # 1
		# spawn_point = carla.Transform(carla.Location(x = 196.86, y = -1.7, z = 1), carla.Rotation(yaw = 90)) # 1
		# spawn_point = carla.Transform(carla.Location(x = 196.86, y = -1.7, z = 1), carla.Rotation(yaw = 90)) # 1
		# spawn_point = carla.Transform(carla.Location(x = 196.86, y = -1.7, z = 1), carla.Rotation(yaw = 90)) # 1
		vehicle = world.try_spawn_actor(blueprint, spawn_point)

	agent = BasicAgent(vehicle, target_speed=30)
	# <Town01>
	# agent.set_destination((92.38, 32.44, 0)) # 1
	agent.set_destination((322.00, 194.70, 0.00)) # 2
	# <Town02>
	# agent.set_destination((45.7, 217.96, 0)) # 1
	# <Town03> Segmentation fault, cannot test !
	# agent.set_destination((45.7, 217.96, 0)) # 1
	# <Town04>
	# agent.set_destination((-493.8, 212.3, 0)) # 1
	# agent.set_destination((228.1, -307.7, 0)) # 2
	# agent.set_destination((228.1, -307.7, 0)) # 3
	# agent.set_destination((228.1, -307.7, 0)) # 4
	# <Town05>
	# agent.set_destination((-47.75, -50, 0)) # 1
	# agent.set_destination((144.8, -2.8, 0)) # 2
	# agent.set_destination((144.84, -1.07, 0)) # 3
	# agent.set_destination((-129.33, 2.86, 0)) # 4
	# <Town06>
	# agent.set_destination((-47.75, -50, 0)) # 1
	# agent.set_destination((-47.75, -50, 0)) # 1
	# agent.set_destination((-47.75, -50, 0)) # 1
	# agent.set_destination((-47.75, -50, 0)) # 1
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
		xv, yv = vehicle.get_location().x, vehicle.get_location().y
		xv, yv = np.round([xv, yv], 2)
		textsurface = myfont.render("X: "+str(xv)+" Y:"+str(yv), True, (0, 0, 0))
		display.blit(textsurface,(1920*0.5*0.1, 1080*0.5*0.9))
		pygame.display.flip()

finally:
	if vehicle is not None:
		vehicle.destroy()
	if camera_sensor is not None:
		camera_sensor.destroy()

