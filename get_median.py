from random import randint
from geo_structures import Point


def get_median(
    points: list[Point], l: int, r: int, k: int, depth: int, K: int
) -> Point:

    pivot = rand_partition(points, l, r, depth, K)
    # wiemy że pivot dzieli liste na w części jedną mniejszą drugą większą

    # Keśli pivot to mediana zwracam go
    if pivot == k:
        return points[pivot]
    elif pivot > k:
        # Szukam mediany w lewej części
        return get_median(points, l, pivot - 1, k, depth, K)
    else:
        # Szukam mediany w prawej części
        return get_median(points, pivot + 1, r, k, depth, K)


def rand_partition(points: list[Point], l: int, r: int, depth: int, K: int) -> int:
    # Wybierz losowy pivot i zamień go z ostatnim elementem
    rand_num = randint(l, r)
    points[rand_num], points[r] = points[r], points[rand_num]

    # Pobierz wartość pivotu (x lub y w zależności od głębokości)
    pivot = points[r].get(depth % K)
    i = l - 1  # Indeks najmniejszego elementu

    # Podziel listę na mniejsze i większe od pivotu
    for j in range(l, r):
        if points[j].get(depth % K) < pivot:
            i += 1
            points[j], points[i] = points[i], points[j]  # Zamień elementy
    i += 1
    points[i], points[r] = points[r], points[i]
    return i
