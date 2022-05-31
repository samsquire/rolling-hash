# based on https://stackoverflow.com/questions/60058670/very-fast-rolling-hash-in-python

import os, random, time
from math import sqrt
from itertools import zip_longest

base = 256
mod  = int(1e9)+7

source = """
i begin the same
but middle differently
but am the same
i am also the same
"""
diff = """
i begin the same
praise the Lord
but am the same
i am the right
i am also the same
"""


def extend(previous_mod, byte):
  return ((previous_mod * base) + ord(byte)) % mod



def remove_left(most_significant, previous_mod, byte):
  return (previous_mod - (most_significant * ord(byte)) % mod) % mod
    
def start_hash(bytes):
  h = 0
  for b in bytes:
      h = extend(h, b)
  return h


def diff_hashes(a, b):
  hashes_left = []
  hashes_right = []
  block_size = int(sqrt(len(a)))
  print(block_size)
  most_significant = pow(base, block_size-1, mod)
  h = start_hash(a[:block_size])
  left_start = block_size
  for i in range(block_size, len(a)):
      h = remove_left(most_significant, h, a[i - block_size])
      h = extend(h, a[i])
      hashes_left.append((h, a[i], i, left_start))
      left_start += -block_size + 1
  h = start_hash(b[:block_size])
  right_start = 0
  for i in range(block_size, len(b)):
      h = remove_left(most_significant, h, b[i - block_size])
      h = extend(h, b[i])
      hashes_right.append((h, b[i], i))
      right_start += -block_size + 1
  start = a[:block_size]
  print(start)
  left_position = 0
  right_position = 0
  missing_right = False
  left_of_right = block_size
  for left, right in zip_longest(hashes_left, hashes_right):
    if left and right:
      if left[0] == right[0]:
        print(left[1], "identical")
        left_position += 1
        right_position += 1
      if left[0] != right[0]:
        print("left only")
        print(left[1])
        left_position += 1
        right_position += 1
    if left and not right:
      missing_right = False
      left_of_right = block_size
      print("unique from left")
      print(left[1])
      left_position += 1
    if right and not left:
      if not missing_right and left_of_right > 0:
        missing = b[right_position-int(block_size/2)+1:right_position+left_of_right]
        print("missing", missing)
        right_position += left_of_right
        left_of_right = 0
        missing_right = True
      else: 
        right_position += 1
      print(right[1], "unique from right")
  return hashes_left

            
diff_hashes(source, diff)
