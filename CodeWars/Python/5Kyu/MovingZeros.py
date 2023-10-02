"""
Write an algorithm that takes an array and moves all of the zeros to the end,
preserving the order of the other elements.

Link: https://www.codewars.com/kata/52597aa56021e91c93000cb0
"""


def move_zeros(lst):
    for number in range(0, lst.count(0)):
        lst.append(lst.pop(lst.index(0)))
    return lst
