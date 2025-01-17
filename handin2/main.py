#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import math


# SOURCE CHARACTER CODING
def inc(e, D):
    if e in D:
        D[e] += 1
    else:
        D[e] = 1


# Format of output: {char1: occurrences1, char2: occurrences2, ...}
def probabilities(fileName):
    output = {}
    with open(fileName) as f:
        c = f.read(1)
        while c:
            inc(c, output)
            c = f.read(1)

    characters = 0
    for key in output:
        characters += output[key]

    for key in output:
        output[key] /= characters

    return output, characters


# HUFFMAN COODING
class Leaf:
    def __init__(self, pair):
        self.char = pair[0]
        self.prob = pair[1]

    def __repr__(self):
        return f"Leaf({self.char}, {self.prob})"


class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.prob = left.prob + right.prob

    def __repr__(self):
        return f"Node({self.left}, {self.right}, {self.prob})"


def huffman(source):
    for i in range(len(source)):
        source[i] = Leaf(source[i])

    while(len(source) > 1):
        x_i = source.pop()
        x_j = source.pop()

        source.append(Node(x_i, x_j))
        source.sort(key=operator.attrgetter("prob"), reverse=True)

    return source[0]


# OUTPUT CODEWORDS
def codewords(huffman, infile, prefix=""):
    if(isinstance(huffman, Leaf)):
        infile.write(f"{repr(huffman.char)}, {huffman.prob:.6f}, {prefix}\n")
    else:
        codewords(huffman.left, infile, f"{prefix}0")
        codewords(huffman.right, infile, f"{prefix}1")


# HUFFMAN NODE TREE TO CODEWORD DICT
def tree2dict(huffman, out={}, prefix=""):
    if(isinstance(huffman, Leaf)):
        out[huffman.char] = len(prefix)
    else:
        tree2dict(huffman.left, out, f"{prefix}0")
        tree2dict(huffman.right, out, f"{prefix}1")
    return out


# HUFFMAN CONVERTER
def encoded_length(fileName, huffdict):
    size = 0
    with open(fileName) as f:
        for line in f:
            for c in line:
                size += huffdict[c]
        f.close()
    return size


# ENTROPY
def entropy(probabilities):
    ent = 0
    for k in probabilities:
        ent += -probabilities[k] * math.log(probabilities[k], 2)
    return ent


if __name__ == '__main__':
    source, characters = probabilities("Alice29.txt")
    print(f"Entropy: {entropy(source):.3f}")
    print(f"Decoded avg length: {8:.3f}, total length: {8 * characters:7}")
    source_sorted = sorted(
        source.items(), key=operator.itemgetter(1), reverse=True)

    huffm = huffman(source_sorted)
    huffdict = tree2dict(huffm)

    enc_len = encoded_length("Alice29.txt", huffdict)
    print(
        f"Encoded avg length: {enc_len / characters:.3f}, total length: {enc_len:7}")

    with open("source.out", "w") as f:
        codewords(huffm, f)
        f.close()
