from __future__ import print_function
import json
import math
import argparse
import xml.etree.ElementTree as ET

import carla
from agents.navigation.local_planner import RoadOption


from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO



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
            waypoint_list.append(carla.Location(x=float(waypoint.attrib['x']),
                                                y=float(waypoint.attrib['y']),
                                                z=float(waypoint.attrib['z'])))

            # Waypoints is basically a list of XML nodes

        list_route_descriptions.append({
            'id': route_id,
                                    'town_name': route_town,
                                    'trajectory': waypoint_list
        })

    return list_route_descriptions

def clean_route(route):

    curves_start_end = []
    inside = False
    start = -1
    current_curve = RoadOption.LANEFOLLOW
    index = 0
    while index < len(route):

        command = route[index][1]
        if command != RoadOption.LANEFOLLOW and not inside:
            inside = True
            start = index
            current_curve = command

        if command != current_curve and inside:
            inside = False
            # End now is the index.
            curves_start_end.append([start, index, current_curve])
            if start == -1:
                raise ValueError("End of curve without start")

            start = -1
        else:
            index += 1

    return curves_start_end

# Draw waypoints with curves
def draw_waypoints( world, waypoints, clean_route, vertical_shift, persistency=-1):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.
    :param waypoints: list or iterable container with the waypoints to draw
    :param vertical_shift: height in meters
    :return:
    """

    for w in waypoints:
        wp = w[0].location + carla.Location(z=vertical_shift)
        world.debug.draw_point(wp, size=0.1, color=carla.Color(0, 255, 0), life_time=persistency)

    for start, end, conditions in clean_route:

        if conditions == RoadOption.LEFT:
            color = carla.Color(255, 255, 0)
        elif conditions == RoadOption.RIGHT:
            color = carla.Color(0, 255, 255)
        elif conditions == RoadOption.CHANGELANELEFT:
            color = carla.Color(255, 64, 0)
        elif conditions == RoadOption.CHANGELANERIGHT:
            color = carla.Color(0, 64, 255)
        else:  # STRAIGHT
            color = carla.Color(128, 128, 128)

        for position in range(start, end):
            world.debug.draw_point(waypoints[position][0].location + carla.Location(z=vertical_shift),
                                   size=0.2, color=color, life_time=persistency)



    world.debug.draw_point(waypoints[0][0].location + carla.Location(z=vertical_shift), size=0.2,
                                color=carla.Color(0, 0, 255), life_time=persistency)
    world.debug.draw_point(waypoints[-1][0].location + carla.Location(z=vertical_shift), size=0.2,
                                color=carla.Color(255, 0, 0), life_time=persistency)

def take_route_picture(world, waypoints):
    wp_location = waypoints[len(waypoints)//2][0].location
    spectator = world.get_spectator()

    spectator.set_transform(carla.Transform(wp_location + carla.Location(z=250),
                                            carla.Rotation(pitch=-90)))



def interpolate_trajectory(world, waypoints_trajectory, hop_resolution=2.0):
    """
        Given some raw keypoints interpolate a full dense trajectory to be used by the user.
    :param world: an reference to the CARLA world so we can use the planner
    :param waypoints_trajectory: the current coarse trajectory
    :param hop_resolution: is the resolution, how dense is the provided trajectory going to be made
    :return: the full interpolated route both in GPS coordinates and also in its original form.
    """

    dao = GlobalRoutePlannerDAO(world.get_map(), hop_resolution)
    grp = GlobalRoutePlanner(dao)
    grp.setup()
    # Obtain route plan
    route = []
    for i in range(len(waypoints_trajectory) - 1):   # Goes until the one before the last.

        waypoint = waypoints_trajectory[i]
        waypoint_next = waypoints_trajectory[i + 1]
        interpolated_trace = grp.trace_route(waypoint, waypoint_next)

        for wp_tuple in interpolated_trace:
            route.append((wp_tuple[0].transform, wp_tuple[1]))

    # Increase the route position to avoid fails

    return route



if __name__ == '__main__':

    DESCRIPTION = ("")

    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument('--id', default=0, help=' route to plot')

    ARGUMENTS = PARSER.parse_args()

    client = carla.Client('localhost', 2000)

    client.set_timeout(25)

    # route = parse_routes_file('/home/praveen/workspace/carla-challenge-contents/src/Town08.xml')
    # route = parse_routes_file('/home/praveen/workspace/scenario_runner/srunner/challenge/routes_training.xml')
    route = parse_routes_file('/home/praveen/workspace/carla-code-pad/corrected_routes.xml')
    world = client.load_world(route[int(ARGUMENTS.id)]['town_name'])
    world.wait_for_tick()

    trajectory = interpolate_trajectory(world, route[int(ARGUMENTS.id)]['trajectory'])
    painted_points = clean_route(trajectory)
    print (painted_points)


    draw_waypoints(world, trajectory, painted_points, vertical_shift=1.0, persistency=50000.0)

    take_route_picture(world, trajectory)
