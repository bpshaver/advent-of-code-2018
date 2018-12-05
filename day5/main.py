from string import ascii_lowercase
from timeit import timeit

sample = 'dabAcCaCBAcCcaDA'

# Part 1
def react_polymer(polymer=sample):
    string_len_pre = len(polymer)
    string_len_post = 0
    while string_len_pre > string_len_post:
        string_len_pre = len(polymer)
        for letter in ascii_lowercase:
            pair = letter + letter.upper()
            polymer = polymer.replace(pair, '')
            polymer = polymer.replace(pair[::-1],'')
        string_len_post = len(polymer)
    return polymer

assert len(react_polymer(sample)) == 10

# RECURSIVE SOLUTION
def left_bisect(string, i):
    if i >= len(string):
        return string
    else:
        return string[:i]

def right_bisect(string, j):
    return string[j+1:]

def recursive_react_polymer(polymer=sample, verbose=False):
    """
    This way hits maximum recursion depth.
    """
    for i, j in zip(range(len(polymer)-1), range(1,len(polymer))):
        if polymer[i] != polymer[j] and polymer[i].lower() == polymer[j].lower():
            left_bisection  = left_bisect(polymer, i)
            right_bisection = right_bisect(polymer, j)
            if verbose:
                print(f"Detected matching pair {polymer[i],polymer[j]}")
                print(f"In string {polymer}:")
                print(f"--{left_bisection}|{polymer[i]}{polymer[j]}|{right_bisection}")
                print('\n')
            recurse_left = recursive_react_polymer(left_bisection, verbose=verbose)
            recurse_right = recursive_react_polymer(right_bisection, verbose=verbose)
            polymer = recursive_react_polymer(recurse_left + recurse_right, verbose=verbose)
            break
        elif j == len(polymer):
            return polymer
    return polymer
    
assert len(recursive_react_polymer(sample)) == 10

# Part 2
def find_smallest_polymer_possible(polymer):
    reaction_sizes = []
    for letter in ascii_lowercase:
        tmp_polymer = polymer.replace(letter,'').replace(letter.upper(), '')
        reaction_sizes.append(len(react_polymer(tmp_polymer)))

    return min(reaction_sizes)

assert find_smallest_polymer_possible(sample) == 4


def main():
    with open('input.txt', 'r') as f:
        polymer = f.read().strip()

    assert len(set(polymer)) == 52
    assert len(set(polymer.lower())) == 26
    part_1 = len(react_polymer(polymer))
    part_2 = find_smallest_polymer_possible(polymer)
    return part_1, part_2

if __name__ == '__main__':
    part_1, part_2 = main()
    print(part_1, part_2)
