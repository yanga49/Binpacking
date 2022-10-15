from typing import Iterator

# Offline algorithms works on a set: they know all the values
WeightSet = (int, list[int])

# Online algorithms work on an iterator: they discover the values on-the-fly
WeightStream = (int, Iterator[int])

# Solution as a list of bins, each one being a list of objects
Solution = list[list[int]]
