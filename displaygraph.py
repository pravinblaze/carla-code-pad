import carla
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import sys
sys.path.append('/home/praveen/workspace/carla/PythonAPI/carla/agents/navigation/')

from local_planner import RoadOption
from global_route_planner import GlobalRoutePlanner
from global_route_planner_dao import GlobalRoutePlannerDAO

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

dao = GlobalRoutePlannerDAO(world_map)
grp = GlobalRoutePlanner(dao)
grp.setup()

for edge in grp._graph.edges():
    n1, n2 = edge
    l1 = grp._graph.nodes[n1]['vertex']
    l2 = grp._graph.nodes[n2]['vertex']
    x1, y1, _ = l1
    x2, y2, _ = l2
    x1, x2 = -x1, -x2
    edge_obj = grp._graph.edges[n1, n2]
    if grp._graph.edges[n1,n2]['type'].value == RoadOption.LANEFOLLOW.value:
        if edge_obj['intersection']:
            plt.plot([x1, x2], [y1, y2], color='red')
        else:
            plt.plot([x1, x2], [y1, y2], color='gray')
    else:
        plt.plot([x1, x2], [y1, y2], color='yellow')
    if n1 != n2:
        plt.arrow(x1, y1, ((x2+x1)/2 - x1), ((y2+y1)/2 - y1), shape='full', lw=0, length_includes_head=True, head_width=2)
    else:
        print "Found loop ", n1, (x1, y1)
    plt.annotate('(%s)' % n1, xy=(x1, y1), textcoords='data')
    plt.annotate('(%s)' % n2, xy=(x2, y2), textcoords='data')

plt.show()
