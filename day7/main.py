from collections import namedtuple
import re

Node = namedtuple('Node', ['parents','children'])

def read_sample():
    sample = """
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    """.strip().split('\n')
    return [string.strip() for string in sample]

def read_input():
    with open('input.txt', 'r') as file:
        inpt = file.read()
    return inpt.strip().split('\n')

def parse_instruction(instruction):
    rgx = 'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
    match = re.match(rgx, instruction)
    if match:
        parent, child = match.groups()
        return parent, child

def generate_graph(instructions):
    nodes = {}
    for instruction in instructions:
        parent, child = parse_instruction(instruction)
        if parent not in nodes:
            nodes[parent] = Node([],[])
        if child not in nodes:
            nodes[child] = Node([],[])
        nodes[parent].children.append(child)
        nodes[child].parents.append(parent)
    return nodes

def find_path(nodes):
    path = []
    while nodes:
        start_nodes = [ID for ID, node in nodes.items() if not node.parents]
        start_nodes.sort(reverse=True)

        next_step = start_nodes.pop()
        nodes.pop(next_step)
        path.append(next_step)
        for node in nodes.values():
            if next_step in node.parents:
                node.parents.remove(next_step)
    return ''.join(path)

if __name__ == '__main__':
    sample = read_sample()
    nodes = generate_graph(sample)
    path = find_path(nodes)
    assert path == 'CABDFE'

    inpt = read_input()
    nodes = generate_graph(inpt)
    path = find_path(nodes)
    print(f"Answer to part 1: {path}")
