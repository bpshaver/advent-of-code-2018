from string import ascii_lowercase
from timeit import timeit


with open('input.txt', 'r') as f:
    polymer = f.read().strip()

assert len(set(polymer)) == 52
assert len(set(polymer.lower())) == 26

sample = 'dabAcCaCBAcCcaDA'

# Part 1
def old_react_polymer(polymer=sample):
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

assert len(old_react_polymer(sample)) == 10

# RECURSIVE SOLUTION
# sample = 'dabAcCaCBAcCcaDA'
# def react_polymer(polymer=sample, verbose=False):
#     for i, pair in enumerate(zip(polymer[:-1], polymer[1:])):
#         letter1, letter2 = pair
#         if letter1 != letter2 and letter1.lower() == letter2.lower():
#             polymer = polymer[:i] + polymer[i+2:]
#             if verbose:
#                 print(f"Found matching pair {pair} at position {i}")
#                 print(f"Recursing with string {polymer[:i]}|{letter1}{letter2}|{polymer[i+2:]} ==> {polymer}")
            
#             polymer = react_polymer(polymer)
#     return polymer

# print(react_polymer(sample, verbose=True))

# assert len(react_polymer(sample)) == 10
# old_time = timeit(old_react_polymer, setup='pass', number=100)
# recursive_time = timeit(react_polymer, setup='pass', number=100)
# assert recursive_time < old_time

# Part 2
def find_smallest_polymer_possible(polymer):
    reaction_sizes = []
    for letter in ascii_lowercase:
        tmp_polymer = polymer.replace(letter,'').replace(letter.upper(), '')
        reaction_sizes.append(len(old_react_polymer(tmp_polymer)))

    return min(reaction_sizes)

assert find_smallest_polymer_possible(sample) == 4

print(find_smallest_polymer_possible(polymer))
