from __future__ import annotations


class Point:
    def __init__(self, x, y):
        # Punkt w dwuwymiarowej przestrzeni
        self.x = x
        self.y = y

    def __str__(self):
        # Reprezentacja punktu jako tekst
        return f"Point({self.x}, {self.y})"

    def get(self, dim):
        if dim == 0:
            return self.x
        else:
            return self.y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))


class RectangleArea:
    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def get_extrema(self):
        return (self.min_x, self.min_y, self.max_x, self.max_y)

    def __eq__(self, other: RectangleArea) -> bool:
        if not isinstance(other, RectangleArea):
            return False
        return self.get_extrema() == other.get_extrema()

    def __and__(self, other: RectangleArea) -> RectangleArea | None:
        min_x = max(self.min_x, other.min_x)
        max_x = min(self.max_x, other.max_x)
        min_y = max(self.min_y, other.min_y)
        max_y = min(self.max_y, other.max_y)
        if min_x <= max_x and min_y <= max_y:
            return RectangleArea(min_x, min_y, max_x, max_y)
        else:
            return None

    def __contains__(self, item: RectangleArea | Point) -> bool:
        if isinstance(item, RectangleArea):
            return self & item == item
        else:
            return (
                self.min_x <= item.x <= self.max_x
                and self.min_y <= item.y <= self.max_y
            )
