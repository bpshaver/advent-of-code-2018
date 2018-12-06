sample = [(1, 1),
(1, 6),
(8, 3),
(3, 4),
(5, 5),
(8, 9)]

with open('input.txt', 'r') as file:
    inpt = file.read().strip().split('\n')
inpt = [string.split(', ') for string in inpt]
inpt = list(zip([int(x[0]) for x in inpt],
                [int(x[1]) for x in inpt]))

import numpy as np
from scipy.spatial.distance import cityblock
from collections import namedtuple

Point = namedtuple('Point', ['id', 'row', 'col','edge'])

ids = list(range(1, len(sample) + 1))
cols = [datum[0] for datum in sample]
rows = [datum[1] for datum in sample]

# ids = list(range(len(inpt)))
# cols = [datum[0] for datum in inpt]
# rows = [datum[1] for datum in inpt]

rectangle = np.zeros((max(rows), max(cols)), dtype=int)

points = []
for point in zip(ids, rows, cols):
    points.append(Point(point[0], point[1] - 1, point[2] - 1,
    point[1] == rectangle.shape[0] or point[2] == rectangle.shape[1] or
    point[1] == 1 or point[2] == 1))

# Part 1 

def find_closest_point(coord, points=points):
    closest_points = [(point, cityblock(coord, (point.row, point.col)))
                        for point in points]
    closest_points.sort(key=lambda x: x[1])
    if closest_points[0][1] == closest_points[1][1]:
        # Tie
        return 0
    else:
        return closest_points[0][0].id

for row in range(rectangle.shape[0]):
    for col in range(rectangle.shape[1]):
        rectangle[(row, col)] = find_closest_point((row,col))

print(rectangle)

from collections import Counter
c = Counter(rectangle.ravel())

disallowed_areas = set([0]).union(rectangle[0]).union(rectangle[:,0]).union(rectangle[-1]).union(rectangle[:,-1])

biggest_area = max([c[point.id] for point in points if point.id not in disallowed_areas])
print(biggest_area)

# Part 2
rectangle = np.zeros((max(rows), max(cols)), dtype=int)

def find_sum_distances(coord, points=points):
    distances = [cityblock(coord, (point.row, point.col))
                        for point in points]
    return sum(distances)
