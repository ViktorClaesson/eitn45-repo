#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator


# SOURCE CHARACTER CODING
def inc(elem, dict):
    if elem in dict:
        dict[elem] += 1
    else:
        dict[elem] = 1


# Format of output: {char1: occurrences1, char2: occurrences2, ...}
def probabilities(fileName):
    output = {}
    with open(fileName) as f:
        c = f.read(1)
        while c:
            inc(c, output)
            c = f.read(1)

    sum = 0
    for key in output:
        sum += output[key]

    for key in output:
        output[key] /= sum

    return output


# HUFFMAN COODING
class Leaf:
    def __init__(self, input):
        self.char = input[0]
        self.prob = input[1]

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


# OUTPuT CODEWORDS
def codewords(file, huffman, prefix):
    if(isinstance(huffman, Leaf)):
        file.write(f"{repr(huffman.char)}, {huffman.prob:.6f}, {prefix}\n")
    else:
        codewords(f, huffman.left, f"{prefix}0")
        codewords(f, huffman.right, f"{prefix}1")


# HUFFMAN CONVERTER
def encode():
    print("encode")


if __name__ == '__main__':
    source = probabilities("Alice29.txt")
    source_sorted = sorted(
        source.items(), key=operator.itemgetter(1), reverse=True)

    huffm = huffman(source_sorted)

    with open("source.out", "w") as f:
        codewords(f, huffm, "")
        f.close()
