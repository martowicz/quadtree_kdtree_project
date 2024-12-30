from random import randint
from geo_structures import Point

K=2




def partition(points: list[Point], l: int, r: int, depth: int) -> int:


    pivot = points[r].get(depth % K)
    i = l - 1
    for j in range(l, r):
        if points[j].get(depth % K) < pivot:
            i += 1
            points[j], points[i] = points[i], points[j]
    i += 1
    points[i], points[r] = points[r], points[i]
    return i



def rand_partition(points: list[Point], l: int, r: int, depth: int) -> int:
    rand_num = randint(l, r)
    points[rand_num], points[r] = points[r], points[rand_num]
    return partition(points, l, r, depth)


def quick_select(points: list[Point], l: int, r: int, k: int, depth: int) -> Point:
    pivot = rand_partition(points, l, r, depth)
    if pivot == k:
        return points[pivot]
    if pivot > k:
        return quick_select(points, l, pivot - 1, k, depth)
    return quick_select(points, pivot + 1, r, k, depth)
