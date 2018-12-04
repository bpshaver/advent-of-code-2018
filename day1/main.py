

def main():
    with open('input.txt', 'r') as file:
        inpt = file.read()

    # Part 1

    freq = 0
    for num in inpt.split():
        freq += int(num)

    # Part 2

    from itertools import cycle
    cycle_inpt = cycle(inpt.split())

    observed_freqs = {0}
    freqfreq = 0
    for num in cycle_inpt:
        freqfreq += int(num)
        if freqfreq in observed_freqs:
            break
        else:
            observed_freqs.add(freqfreq)


    return freq, freqfreq

if __name__ == '__main__':
    freq, freqfreq = main()
    print(freq)
    print(freqfreq)
