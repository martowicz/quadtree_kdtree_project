from random import randint
from geo_structures import Point


# Funkcja rand_partition
def rand_partition(points: list[Point], l: int, r: int, depth: int, K: int) -> int:
    """
    Wybiera losowy pivot, zamienia go z ostatnim elementem, a następnie wywołuje `partition`.

    Args:
        points: Lista punktów do podziału.
        l: Indeks początkowy (lewy).
        r: Indeks końcowy (prawy).
        depth: Głębokość w drzewie KD, używana do wyboru wymiaru podziału.

    Returns:
        Indeks pivota po podziale.
    """
    rand_num = randint(l, r)  # Wybierz losowy indeks pomiędzy l a r
    points[rand_num], points[r] = points[r], points[rand_num]

     # Zamień losowy pivot z ostatnim elementem

    """
    Dzieli listę punktów w taki sposób, że wszystkie elementy mniejsze od pivota znajdują się
    po lewej stronie, a większe po prawej stronie.

    Args:
        points: Lista punktów do podziału.
        l: Indeks początkowy (lewy).
        r: Indeks końcowy (prawy).
        depth: Głębokość w drzewie KD, używana do wyboru wymiaru podziału.

    Returns:
        Indeks pivota po podziale.
    """
    pivot = points[r].get(
        depth % K
    )  # Pobierz wartość pivotu (x lub y w zależności od głębokości)
    i = l - 1  # Indeks dla mniejszych elementów
    for j in range(l, r):
        # Jeśli bieżący element jest mniejszy od pivotu
        if points[j].get(depth % K) < pivot:
            i += 1
            points[j], points[i] = points[i], points[j]  # Zamień elementy
    i += 1
    points[i], points[r] = points[r], points[i]  # Umieść pivot na właściwej pozycji
    return i  # Zwróć indeks pivota



def get_median(points: list[Point], l: int, r: int, k: int, depth: int, K: int):
    """
    Funkcja median która znajduje medianę w liście punktów w danym wymiarze.

    Argumenty:
        points - Lista punktów do podziału.
        depth - Głębokość w drzewie KD.
        K - Wymiar drzewa KD
    """

    pivot = rand_partition(points, l, r, depth, K)  # Podziel listę i znajdź pivot

    if pivot == k:
        return points[pivot]  # znaleźliśmy mediane
    elif pivot > k:
        return get_median(points, l, pivot - 1, k, depth, K)
    else:
        return get_median(points, pivot + 1, r, k, depth, K)
