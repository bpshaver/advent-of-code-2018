import numpy as np
import re
import matplotlib.pyplot as plt

LENGTH = 1000
WIDTH  = 1000

def parse_claim(claim):
    id_regex = re.compile('(?<=#)\d+')
    left_regex = re.compile('(?<=@ )\d+')
    top_regex = re.compile('(?<=\d,)\d+')
    width_regex = re.compile('(?<=: )\d+')
    length_regex = re.compile('(?<=\dx)\d+')

    id = int(re.search(id_regex, claim).group(0))
    left = int(re.search(left_regex, claim).group(0))
    top = int(re.search(top_regex, claim).group(0))
    width = int(re.search(width_regex, claim).group(0))
    length = int(re.search(length_regex, claim).group(0))

    return dict(id=id, left=left, top=top, width=width, length=length)

def main():
    with open('input.txt', 'r') as file:
        claims = file.read().strip().split('\n')

    # Part 1
    fabric = np.zeros((LENGTH, WIDTH))

    for claim in claims:
        claim = parse_claim(claim)
        for row in range(claim['length']):
            for column in range(claim['width']):
                fabric[(row + claim['top'], column + claim['left'])] += 1

    bool_fabric = np.vectorize(bool)(fabric)
    num_covered = np.sum(bool_fabric)

    plt.imshow(fabric, cmap='seismic_r', interpolation='nearest')
    plt.show()



    return num_covered, _

if __name__ == '__main__':
    num_covered, _ = main()
    print(num_covered)
