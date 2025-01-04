from __future__ import annotations
from get_median import get_median
from geo_structures import RectangleArea, Point

K = 2


class KdTreeNode:
    def __init__(self, axis: int | None, rectangle: RectangleArea) -> None:

        self.axis = axis  # określa którą oś rozpatrujemy tj. dla K=2 czy wedługo osi X czy Y/
        self.rectangle = rectangle  # obszar który jesr reprezentowany przez poddtrzewo tego wierzchołka
        self.left_node = None  # lewe dziecko
        self.right_node = None  # prawe dziecko
        self.leafs_list = []  # list liści w poddrzewie
        self.leaf_point = None  # jeśli node jest liście to znajduje się tu punkt


class KdTree:
    def __init__(self, points: list[Point]):

        self.points = points
        self.max_rectangle = RectangleArea(
            min(points, key=lambda p: p.x).x,  # Minimalna wartość x
            min(points, key=lambda p: p.y).y,  # Minimalna wartość y
            max(points, key=lambda p: p.x).x,  # Maksymalna wartość x
            max(points, key=lambda p: p.y).y,  # Maksymalna wartość y
        )
        self.root = self.build_tree(self.points, 0, self.max_rectangle)

    def build_tree(
        self, points: list[Point], depth: int, rectangle: RectangleArea
    ) -> KdTreeNode:

        # Jeśli w poddrzewie jest 1 punkt, to jest to liść
        if len(points) == 1:
            node = KdTreeNode(None, rectangle)
            node.leaf_point = points[0]
            return node

        p_smaller = []  # lista na punkt mniejsze od mediany
        p_larger = []

        median_point = get_median(
            points, 0, len(points) - 1, (len(points) - 1) // 2, depth, K
        )

        # Mediana w wymiarze
        median = median_point.get(depth % K)

        # Wrzuca punkty na lewo i prawo od mediany
        balanser = 0  # balansuje drzewo

        for point in points:
            if point.get(depth % K) < median:
                p_smaller.append(point)
            elif point.get(depth % K) > median:
                p_larger.append(point)
            else:
                if balanser % 2 == 0:
                    p_smaller.append(point)
                else:
                    p_larger.append(point)
                balanser += 1

        # print(p_smaller," _ ",p_larger)

        min_x, min_y, max_x, max_y = rectangle.get_extrema()
        if depth % K == 0:  # Podział wzdłuż osi x
            node_smaller = self.build_tree(
                p_smaller, depth + 1, RectangleArea(min_x, min_y, median, max_y)
            )
            node_larger = self.build_tree(
                p_larger, depth + 1, RectangleArea(median, min_y, max_x, max_y)
            )
        else:  # Podział wzdłuż osi y
            node_smaller = self.build_tree(
                p_smaller, depth + 1, RectangleArea(min_x, min_y, max_x, median)
            )
            node_larger = self.build_tree(
                p_larger, depth + 1, RectangleArea(min_x, median, max_x, max_y)
            )

        # łączymy postrekurenycjnie noda z jego dziećmi
        node = KdTreeNode(depth, rectangle)
        node.left_node = node_smaller
        node.right_node = node_larger

        if node.left_node.leaf_point is not None:
            node.leafs_list.append(node_smaller)
        else:
            node.leafs_list.extend(node.left_node.leafs_list)

        if node.right_node.leaf_point is not None:
            node.leafs_list.append(node_larger)
        else:
            node.leafs_list.extend(node.right_node.leafs_list)

        return node

    def find_recursive(
        self, node: KdTreeNode, rectangle: RectangleArea, res: list[Point]
    ):
        if (
            rectangle & node.rectangle is None
        ):  # szukany obaszar jest poza obecnym obszarem
            return
        if node.leaf_point is not None and node.leaf_point in rectangle:
            res.append(
                node.leaf_point
            )  # node jest liściem i jest w obszarze więc dodajemy
            return
        for leaf_node in node.leafs_list:  # wchodzimy głębiej
            self.find_recursive(leaf_node, rectangle, res)

    def find(self, rectangle: RectangleArea) -> list[Point]:
        res = []
        self.find_recursive(self.root, rectangle, res)
        return res
