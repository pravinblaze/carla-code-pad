import carla
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import sys
sys.path.append('/home/praveen/programs/carla/PythonAPI/agents/navigation/')

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
    x1, y1 = grp._graph.nodes[n1]['vertex']
    x2, y2 = grp._graph.nodes[n2]['vertex']
    x1, x2 = -x1, -x2
    plt.plot([x1, x2], [y1, y2])
    plt.arrow(x1, y1, (x2+x1)/2 - x1, (y2+y1)/2 - y1,
    shape='full', lw=0, length_includes_head=True, head_width=2)
    plt.annotate('(%s)' % n1, xy=(x1, y1), textcoords='data')
    plt.annotate('(%s)' % n2, xy=(x2, y2), textcoords='data')

plt.show()
