# Hell yeah !

import os
import random
import sys
import xml.etree.ElementTree as ET

import numpy as np
import carla
from carla import ColorConverter as cc
import pygame

from agents.navigation.basic_agent import BasicAgent
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO

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

dao = GlobalRoutePlannerDAO(world_map)
grp = GlobalRoutePlanner(dao)
grp.setup()

route_filename = '/home/praveen/workspace/scenario_runner/srunner/challenge/routes_training.xml'
route_index = '1'

def parse_routes_file(route_filename):
    """
    Returns a list of route elements that is where the challenge is going to happen.
    :param route_filename: the path to a set of routes.
    :return:  List of dicts containing the waypoints, id and town of the routes
    """

    list_route_descriptions = []
    tree = ET.parse(route_filename)
    for route in tree.iter("route"):
        route_town = route.attrib['map']
        route_id = route.attrib['id']
        waypoint_list = []  # the list of waypoints that can be found on this route
        for waypoint in route.iter('waypoint'):
             waypoint_list.append(waypoint)  # Waypoints is basically a list of XML nodes

        list_route_descriptions.append({
                                    'id': route_id,
                                    'town_name': route_town,
                                    'trajectory': waypoint_list
                                     })

    return list_route_descriptions

def interpolate_trajectory(global_router, waypoints_trajectory, hop_resolution = 2.0):
    """
        Given some raw keypoints interpolate a full dense trajectory to be used by the user.
    :param world: an reference to the CARLA world so we can use the planner
    :param waypoints_trajectory: the current coarse trajectory
    :param hop_resolution: is the resolution, how dense is the provided trajectory going to be made
    :return: the full interpolated robuild_master_scenarioute both in GPS coordinates and also in its original form.
    """

    # Obtain route plan
    route = []
    for i in range(len(waypoints_trajectory) - 1):   # Goes until the one before the last.

		waypoint = waypoints_trajectory[i]
		waypoint_next = waypoints_trajectory[i+1]
		interpolated_trace = global_router.trace_route(carla.Location(x=float(waypoint.attrib['x']),
												y=float(waypoint.attrib['y']),
												z=float(waypoint.attrib['z'])),
									carla.Location(x=float(waypoint_next.attrib['x']),
												y=float(waypoint_next.attrib['y']),
												z=float(waypoint_next.attrib['z']))
									)
		route += interpolated_trace
    return route

try:

	# Select trajectory
	route_list = parse_routes_file(route_filename)
	route = None
	for route_candidate in route_list:
		if route_candidate['id'] == route_index:
			route = route_candidate['trajectory']
			break
	dense_route_trace = interpolate_trajectory(grp, route)

	vehicle = None
	world_actors = world.get_actors().filter('vehicle.*')
	print("Number of actors ", len(world.get_actors().filter('vehicle.*')))
	for actor in world_actors:
		print("Found actor with role", actor.attributes['role_name'])
		if actor.attributes['role_name'] == 'hero':
			print("Found hero vehicle")
			vehicle = actor

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

	waypoint_index = 0
	while True:
		control = vehicle.get_control()
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
		# HUD
		current_location_surface = myfont.render("Throttle: "+str(control.throttle), True, (0, 0, 0))
		next_location = route[waypoint_index]
		next_location = carla.Location(
			float(next_location.attrib['x']),
			float(next_location.attrib['y']),
			float(next_location.attrib['z']))
		next_location_surface = myfont.render("Steer: "+str(control.steer), True, (0, 0, 0))
		display.blit(current_location_surface,(1920*0.5*0.05, 1080*0.5*0.8))
		display.blit(next_location_surface,(1920*0.5*0.05, 1080*0.5*0.9))
		if vehicle.get_location().distance(next_location) < 10 and waypoint_index+1 < len(route):
			waypoint_index += 1
		pygame.display.flip()

finally:
	if vehicle is not None:
		vehicle.destroy()
	if camera_sensor is not None:
		camera_sensor.destroy()
