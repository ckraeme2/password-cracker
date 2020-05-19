#!/usr/bin/env python3

import concurrent.futures
import hashlib
import os
import string
import sys

# Constants

ALPHABET = string.ascii_lowercase + string.digits

# Functions

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def md5sum(s):
    ''' Compute md5 digest for given string. '''
    # TODO: Use the hashlib library to produce the md5 hex digest of the given
    # string.
    checksum = hashlib.md5(s.encode())

    return checksum.hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of the given length using the
    provided alphabet. '''
    # TODO: Use yield to create a generator function that recursively produces
    # all the permutations of the given length using the provided alphabet.
    if length == 0:
        yield None
    if length == 1:
        for char in alphabet:
            yield char
    else:
        for char in alphabet:
            for permutation in permutations(length-1,alphabet):
                yield char+permutation

def flatten(sequence):
    ''' Flatten sequence of iterators. '''
    # TODO: Iterate through sequence and yield from each iterator in sequence.
    for seq in sequence:
        for item in seq:
            yield item

def crack(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes
    by sequentially trying all permutations. '''
    # TODO: Return list comprehension that iterates over a sequence of
    # candidate permutations and checks if the md5sum of each candidate is in
    # hashes.

    return [candidate for candidate in [prefix+permutation for permutation in permutations(length, alphabet)] if md5sum(candidate) in hashes] 
    
def cracker(arguments):
    ''' Call the crack function with the specified arguments '''
    return crack(*arguments)

def smash(hashes, length, alphabet=ALPHABET, prefix='', cores=1):
    ''' Return all password permutations of specified length that are in hashes
    by concurrently subsets of permutations concurrently.
    '''
    # TODO: Create generator expression with arguments to pass to cracker and
    # then use ProcessPoolExecutor to apply cracker to all items in expression.

    arguments = ((hashes, length-1, alphabet, prefix+char) for char in alphabet)

    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
        results = executor.map(cracker, arguments)


    return flatten(results)

def main():
    arguments   = sys.argv[1:]
    alphabet    = ALPHABET
    cores       = 1
    hashes_path = 'hashes.txt'
    length      = 1
    prefix      = ''

    # TODO: Parse command line arguments
    while len(arguments) > 0:
        argument = arguments.pop(0)

        if argument == '-a':
            alphabet = arguments.pop(0)
        elif argument == '-c':
            cores = int(arguments.pop(0))
        elif argument == '-l':
            length = int(arguments.pop(0))
        elif argument == '-p':
            prefix = arguments.pop(0)
        elif argument == '-s':
            hashes_path = arguments.pop(0)
        else:
            usage(1)
    # TODO: Load hashes set
    hashes = set([line.rstrip() for line in open(hashes_path)])

    # TODO: Execute crack or smash function
    if length > 1 and cores > 1:
        results = smash(hashes,length,alphabet,prefix,cores)
    else:
        results = crack(hashes,length,alphabet,prefix)
    # TODO: Print all found passwords
    for result in results:
        print(result)
# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
