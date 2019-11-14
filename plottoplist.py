import math

import carla
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

client = carla.Client('localhost', 2000)
world = client.get_world()
world_map = world.get_map()
topology = world_map.get_topology()

count = 0
for segment in topology:
	x1, y1 = segment[0].transform.location.x, segment[0].transform.location.y
	x2, y2 = segment[1].transform.location.x, segment[1].transform.location.y
	x1, x2 = -x1, -x2
	if math.sqrt((x2-x1)**2+(y2-y1)**2) > 0.01:
		if segment[0].is_intersection:
			plt.plot([x1, x2], [y1, y2], color='black')
			plt.plot([x1, x2], [y1, y2], 'o')
		else:
			plt.plot([x1, x2], [y1, y2])
			plt.plot([x1, x2], [y1, y2], 'o')
		plt.arrow(x1, y1, (x2+x1)/2 - x1, (y2+y1)/2 - y1,
		shape='full', lw=0, length_includes_head=True, head_width=2)
	else:
		print 'Found zero segment', segment[0].transform.location

plt.show()

