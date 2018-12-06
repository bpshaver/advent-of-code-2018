import numpy as np
from scipy.spatial.distance import cityblock
from collections import namedtuple, Counter

Point = namedtuple('Point', ['id', 'row', 'col','edge'])

def find_closest_point(coord, points):
    closest_points = [(point, cityblock(coord, (point.row, point.col)))
                        for point in points]
    closest_points.sort(key=lambda x: x[1])
    if closest_points[0][1] == closest_points[1][1]:
        # Tie
        return 0
    else:
        return closest_points[0][0].id

def find_sum_distances(coord, points):
    distances = [cityblock(coord, (point.row, point.col))
                        for point in points]
    return sum(distances)

def main(data, threshold):

    ids = list(range(1, len(data) + 1))
    cols = [datum[0] for datum in data]
    rows = [datum[1] for datum in data]

    rectangle = np.zeros((max(rows), max(cols)), dtype=int)

    points = []
    for point in zip(ids, rows, cols):
        points.append(Point(point[0], point[1] - 1, point[2] - 1,
        # Check if the point is on an edge:
        point[1] == rectangle.shape[0] or
        point[2] == rectangle.shape[1] or
        point[1] == 1 or point[2] == 1))

    # Part 1
    for row in range(rectangle.shape[0]):
        for col in range(rectangle.shape[1]):
            rectangle[(row, col)] = find_closest_point((row,col), points)
    c = Counter(rectangle.ravel())

    disallowed_areas = set([0]).union(rectangle[0]).union(
        rectangle[:,0]).union(rectangle[-1]).union(rectangle[:,-1])

    biggest_area = max([c[point.id] for point in points if point.id
                                            not in disallowed_areas])

    # Part 2
    rectangle = np.zeros((max(rows), max(cols)), dtype=int)



    for row in range(rectangle.shape[0]):
        for col in range(rectangle.shape[1]):
            rectangle[(row, col)] = find_sum_distances(
                                        (row,col), points) < threshold

    biggest_remote_area = np.sum(rectangle)

    return biggest_area, biggest_remote_area

if __name__ == '__main__':
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

    assert 17, 16 == main(sample, 32)

    part1, part2 = main(inpt, 10000)
    print(part1, part2)
