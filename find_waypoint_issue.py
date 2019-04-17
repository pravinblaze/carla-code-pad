# Hell yeah !

import xml.etree.ElementTree as ET
import carla

from agents.navigation.basic_agent import BasicAgent
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

dao = GlobalRoutePlannerDAO(world_map)
grp = GlobalRoutePlanner(dao)
grp.setup()

# route_filename = '/home/praveen/workspace/carla-challenge-contents/src/Town08.xml'
route_filename = '/home/praveen/workspace/scenario_runner/srunner/challenge/routes_training.xml'
index_start = 0
index_end = 9
output_path = "/home/praveen/workspace/carla-code-pad/waypoint_issues_town01.txt"

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

route_list = parse_routes_file(route_filename)
s = "Waypoints that localize to an intersection segment. \n\n"
for route_candidate in route_list:
    if int(route_candidate['id']) >= index_start and \
        int(route_candidate['id']) <= index_end:
        s += "Route ID : " + route_candidate['id'] + "\n\n"
        for point in route_candidate['trajectory']:
            location = carla.Location(
                float(point.attrib['x']),
                float(point.attrib['y']),
                float(point.attrib['z']))
            edge_nodes = grp._localize(location)
            if edge_nodes is not None:
                n1, n2 = edge_nodes
                if n1 > -1 and n2 > -1:
                    edge = grp._graph.edges[n1, n2]
                    if edge['intersection']:
                        s += point.attrib['x'] + "  "
                        s += point.attrib['y'] + "  "
                        s += point.attrib['z']
                        s += "\n"
    s += "\n\n"

with open(output_path, "w") as f:
    f.write(s)
    f.close()

print("DONE !")
