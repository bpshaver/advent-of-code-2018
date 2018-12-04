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

    id = re.search(id_regex, claim).group(0)
    left = int(re.search(left_regex, claim).group(0))
    top = int(re.search(top_regex, claim).group(0))
    width = int(re.search(width_regex, claim).group(0))
    length = int(re.search(length_regex, claim).group(0))

    return dict(id=id, left=left, top=top, width=width, length=length)

def main(inpt='input.txt', width=1000, length=1000, draw=False):
    with open(inpt, 'r') as file:
        claims = file.read().strip().split('\n')

    # Part 1
    fabric = np.zeros((width, length), dtype=int)

    for unparsed_claim in claims:
        claim = parse_claim(unparsed_claim)
        for row in range(claim['length']):
            for column in range(claim['width']):
                fabric[(row + claim['top'], column + claim['left'])] += 1


    bool_fabric = np.vectorize(lambda x: x > 1)(fabric)
    num_covered = np.sum(bool_fabric)
    if draw:
        plt.imshow(fabric, cmap='Reds_r', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.title('Santa\'s Contested Magical Fabric')
        plt.savefig('SantaFabric.png')
        plt.show()

    # Part 2
    # Should be easy by copying most of the above

    for unparsed_claim in claims:
        uncontested = True
        claim = parse_claim(unparsed_claim)
        for row in range(claim['length']):
            for column in range(claim['width']):
                if fabric[(row + claim['top'], column + claim['left'])] > 1:
                    uncontested = False
        if uncontested:
            # Assuming only one winner
            winning_claim = claim


    return num_covered, winning_claim, claims

if __name__ == '__main__':
    # num_covered, winning_claim = main('test.txt', width=8, length=8)
    num_covered, winning_claim, claims = main()
    print(num_covered)
    print(winning_claim)
