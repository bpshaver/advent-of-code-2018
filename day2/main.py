from collections import Counter

def get_string_similarity(s1, s2):
    assert len(s1) == len(s2)
    common = ''.join([pair[0] for pair in zip(s1, s2) if pair[0] == pair[1]])
    return common, len(s1) - len(common)

def main():
    with open('input.txt', 'r') as file:
        inpt = file.read()
    
    # Part 1
    ids = [id for id in inpt.split()]
    num_doubles = 0
    num_triples = 0
    for id in ids:
        c = Counter(id)
        if 2 in c.values():
            num_doubles += 1
        if 3 in c.values():
            num_triples += 1
    checksum = num_doubles * num_triples

    # Part 2
    results = []
    for i, id_i in enumerate(ids):
        for j, id_j in enumerate(ids):
            if i != j:
                results.append(get_string_similarity(id_i, id_j))

    results.sort(key = lambda x: x[1])
    common_letters = results[0][0]
    
    return checksum, common_letters

if __name__ == '__main__':
    checksum, common_letters = main()
    print(checksum)
    print(common_letters)
