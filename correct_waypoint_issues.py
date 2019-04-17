# Hell yeah !

import argparse
import xml.etree.ElementTree as ET

import carla

from agents.navigation.basic_agent import BasicAgent
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO

if __name__ == '__main__':

    DESCRIPTION = ("")
    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument('--file', default='', help='file name to correct')
    ARGUMENTS = PARSER.parse_args()

    client = carla.Client('localhost', 2000)
    client.set_timeout(25)

    print("Commencing xml data correction !")

    routes_xml_data = ET.parse(ARGUMENTS.file)
    corrected_xml_data = ET.Element('routes')
    for route in routes_xml_data.iter("route"):

        map_name = route.get('map')
        world = client.get_world()
        world_map = world.get_map()

        print("Dealing with map : ", map_name)

        if map_name != world_map.name:
            print("Loading map : ", map_name)
            world = client.load_world(map_name)
            world.wait_for_tick()
            world_map = world.get_map()

        dao = GlobalRoutePlannerDAO(world_map)
        grp = GlobalRoutePlanner(dao)
        grp.setup()

        corrected_route = ET.SubElement(corrected_xml_data, 'route')
        corrected_route.set('id', route.get('id'))
        corrected_route.set('map', route.get('map'))
        print("Dealing with route : ", route.get('id'))
        for point in route.iter('waypoint'):
            location = carla.Location(  
                float(point.attrib['x']),
                float(point.attrib['y']),
                float(point.attrib['z']))
            edge_nodes = grp._localize(location)
            if edge_nodes is not None and True:
                n1, n2 = edge_nodes
                if n1 > -1 and n2 > -1:
                    edge = grp._graph.edges[n1, n2]
                    if edge['intersection']:
                        pass
                    else:
                        corrected_route.append(point)
            else:
                corrected_route.append(point)

    with open("routes_devtest_corrected.xml", "w") as f:
        f.write(ET.tostring(corrected_xml_data))
        f.close()

    print("Done correcting ! ")
