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

#####

from string import ascii_uppercase

class Node2():
    def __init__(self, ID, offset=60):
        self.ID = ID
        self.parents = []
        self.children = []
        self.started = False
        self.finished = False
        self.offset = offset
        self.duration = self.get_duration()
        
    def __repr__(self):
        return f"node: {self.ID}, Started: {self.started}, Duration: {self.duration}, Parents: {self.parents}, Children: {self.children}"

    def get_duration(self):
        return ascii_uppercase.index(self.ID) + 1 + self.offset
    
def vprint(string, verbose=False):
    if verbose:
        print(string)

def generate_graph2(instructions, offset=0):
    nodes = {}
    for instruction in instructions:
        parent, child = parse_instruction(instruction)
        if parent not in nodes:
            nodes[parent] = Node2(parent, offset=offset)
        if child not in nodes:
            nodes[child] = Node2(child, offset=offset)
        nodes[parent].children.append(child)
        nodes[child].parents.append(parent)
    return nodes

def do_work(nodes, num_workers, verbose=False):
    workers = dict.fromkeys(range(num_workers))
    done = ''
    second = 0
    while not all([node.finished for node in nodes.values()]):
        vprint(second, verbose=verbose)
        # While not all nodes are finished. Or while nodes?
        for node in nodes.values():
            # For every node:
            if node.started and not node.finished:
                # Let the decrementing happen with the workers
                if node.duration == 0:
                    # The node is finished!
                    vprint(f"Node {node.ID} finished!", verbose=verbose)
                    node.finished = True
                    # Add the node id to the "path" of finished nodes
                    done = done + node.ID
                    # For every child node of the complete node,
                    # remove it as a parent:
                    for child_node in node.children:
                        nodes[child_node].parents.remove(node.ID)
                    ###
        # Get list of available nodes, ready to be worked on:
        available_nodes = [node for node in nodes.values() 
                           if not node.parents and not node.started]
        # Sort in reverse order so we can pop off in alphabetical order:
        available_nodes.sort(reverse=True, key=lambda node: node.ID)
        vprint(f"Available nodes: {available_nodes}", verbose=verbose)
        # Just storing workers as keys in a dict:
        for worker in workers:
            # If the current worker has a task:
            if workers[worker]:
                # If that worker is still working, pass
                if workers[worker].duration > 0:
                    vprint(f"Decrementing node {workers[worker].ID} by 1", verbose=verbose)
                    workers[worker].duration -= 1
                    continue
                # Otherwise, the duration should be zero
                else:
                    assert workers[worker].duration == 0
                    # Set that worker free:
                    workers[worker] = None
            # This can't be elif since the worker may just have been made free
            if available_nodes:
                # Otherwise, assign the worker a task from the available nodes:
                workers[worker] = available_nodes.pop()
                vprint(f"Assigning node {workers[worker].ID} to worker {worker}", verbose=verbose)
                workers[worker].started = True
                # and decrement that node duration by 1:
                workers[worker].duration -= 1
                vprint(f"Decrementing node {workers[worker].ID} by 1", verbose=verbose)
        vprint(f"Done: {done}", verbose=verbose)
        vprint('---', verbose=verbose)
        nodes = {ID:node for ID, node in nodes.items() if not node.finished}
        second += 1

    return done, second - 1

if __name__ == '__main__':
    sample = read_sample()
    nodes = generate_graph(sample)
    path = find_path(nodes)
    assert path == 'CABDFE'

    inpt = read_input()
    nodes = generate_graph(inpt)
    path = find_path(nodes)
    print(f"Answer to part 1: {path}")

    nodes = generate_graph2(sample, offset=0)
    done, seconds = do_work(nodes, num_workers=2,  verbose=True)
    assert done == 'CABFDE'
    assert seconds == 15

    inpt = read_input()
    nodes = generate_graph2(inpt,offset=60)
    done, seconds = do_work(nodes, num_workers=5)
    print(f"Answer to part 2: {seconds}")
