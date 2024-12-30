from __future__ import annotations
from quick_select import quick_select
from geo_structures import RectangleArea, Point
from visualizer.main import Visualizer

K = 2


class KdTreeNode:
    def __init__(self, dim: int | None, rectangle: RectangleArea):
        self.dim = dim
        self.rectangle = rectangle
        self.left = None
        self.right = None
        self.leafs = []
        self.leaf_point = None

    def __str__(self):
        return f"KdTreeNode({self.dim}, {self.leaf_point},{self.rectangle})"


class KdTree:
    def __init__(self, points: list[Point]):
        self.points = list(set(points))

        self.max_rectangle = RectangleArea(
            min(points, key=lambda p: p.x).x,  # Minimalna wartość x
            min(points, key=lambda p: p.y).y,  # Minimalna wartość y
            max(points, key=lambda p: p.x).x,  # Maksymalna wartość x
            max(points, key=lambda p: p.y).y,  # Maksymalna wartość y
        )
        self.vis = Visualizer()
        for point in points:
            self.vis.add_point((point.x, point.y), color='red', s=5)


        self.root = self.build_tree(self.points, 0, self.max_rectangle)

    def build_tree(
        self, points: list[Point], depth: int, rectangle: RectangleArea
    ) -> KdTreeNode:

        # Jeśli w poddrzewie jest 1 punkt, to jest to liść
        if len(points) == 1:
            node = KdTreeNode(None, rectangle)
            node.leaf_point = points[0]
            return node

        p_smaller = []
        p_larger = []

        median_point = quick_select(
            points, 0, len(points) - 1, (len(points) - 1) // 2, depth % K
        )

        # Mediana w danym wymiarze
        median = median_point.get(depth % K)

        # Wrzuca punkty na lewo i prawo od mediany
        # equal_counter balansuje drzewo
        equal_counter = 0
        for point in points:
            if point.get(depth % K) < median:
                p_smaller.append(point)
            elif point.get(depth % K) > median:
                p_larger.append(point)
            else:
                if equal_counter % 2 == 0:
                    p_smaller.append(point)
                else:
                    p_larger.append(point)
                equal_counter += 1

        #print(p_smaller," _____ ",p_larger)

        min_x, min_y, max_x, max_y = rectangle.get_extrema()
        if depth % 2 == 0:  # Podział wzdłuż osi x
            self.vis.add_line_segment(((median, min_y), (median, max_y)), color='black', s=2)

            node_smaller = self.build_tree(
                p_smaller, depth + 1, RectangleArea(min_x, min_y, median, max_y)
            )
            node_larger = self.build_tree(
                p_larger, depth + 1, RectangleArea(median, min_y, max_x, max_y)
            )
        else:  # Podział wzdłuż osi y
            self.vis.add_line_segment(((min_x, median), (max_x, median)), color='black', s=2)

            node_smaller = self.build_tree(
                p_smaller, depth + 1, RectangleArea(min_x, min_y, max_x, median)
            )
            node_larger = self.build_tree(
                p_larger, depth + 1, RectangleArea(min_x, median, max_x, max_y)
            )

        # Tworzymy węzeł wewnętrzny
        node = KdTreeNode(depth, rectangle)
        node.left = node_smaller
        node.right = node_larger

        # Dodajemy liście
        if node_smaller.leaf_point is not None:
            node.leafs.append(node_smaller)
        else:
            node.leafs += node_smaller.leafs

        if node_larger.leaf_point is not None:
            node.leafs.append(node_larger)
        else:
            node.leafs += node_larger.leafs

        return node



    def __find(self, node: KdTreeNode, rectangle: RectangleArea, res: list[Point]):
        if rectangle & node.rectangle is None:
            return
        if len(node.leafs) == 0:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                res.append(node.leaf_point)
            return
        for leaf_node in node.leafs:
            self.__find(leaf_node, rectangle, res)

    def find(self, rectangle: RectangleArea) -> list[Point]:
        res = []
        self.__find(self.root, rectangle, res)
        return res


    def tree_print(self, node: KdTreeNode):
        if node is not None:
            print(node)
            self.tree_print(node.left)
            self.tree_print(node.right)
