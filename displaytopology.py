import glob
import os
import sys

import carla
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()

topology = world_map.get_topology()
for segment in topology:
    x1, y1 = segment[0].transform.location.x, segment[0].transform.location.y
    x2, y2 = segment[1].transform.location.x, segment[1].transform.location.y
    plt.plot([x1, x2], [y1, y2], marker = 'o')
plt.show()
