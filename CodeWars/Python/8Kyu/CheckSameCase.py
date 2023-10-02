"""
Write a function that will check if two given characters are the same case.

- If either of the characters is not a letter, return -1
- If both characters are the same case, return 1
- If both characters are letters, but not the same case, return 0

https://www.codewars.com/kata/5dd462a573ee6d0014ce715b"""


def same_case(a, b):
    if not (a.isalpha() and b.isalpha()):
        return -1
    elif a.isupper() == b.isupper():
        return 1
    elif a.isalpha() and b.isalpha():
        return 0
