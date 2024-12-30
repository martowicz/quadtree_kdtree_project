
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from visualizer.main import Visualizer
from geo_structures import RectangleArea, Point


class QuadtreeNode:
    def __init__(self, rectangle: RectangleArea):
        self.rectangle = rectangle  # Całkowity obszar tego węzła
        self.points = []  # Punkty w tym węźle
        self.upper_left = None  # Lewy górny kwadrant
        self.upper_right = None  # Prawy górny kwadrant
        self.lower_left = None  # Lewy dolny kwadrant
        self.lower_right = None  # Prawy dolny kwadrant
        self.is_leaf = True  # Czy jest liściem (czy ma dzieci)
    
    def __str__(self):
        return f"QuadtreeNode({self.rectangle}, Points={len(self.points)}, is_leaf={self.is_leaf})"

class Quadtree:
    def __init__(self, points: list[Point], max_points_per_node: int = 4):
        self.max_points_per_node = max_points_per_node
        self.max_rectangle = RectangleArea(
            min(points, key=lambda p: p.x).x,  # Minimalna wartość x
            min(points, key=lambda p: p.y).y,  # Minimalna wartość y
            max(points, key=lambda p: p.x).x,  # Maksymalna wartość x
            max(points, key=lambda p: p.y).y,  # Maksymalna wartość y
        )

        
        self.vis = Visualizer()
        for point in points:
            self.vis.add_point((point.x, point.y), color='red', s=5)

        self.root = self.build_tree(self.max_rectangle, points)

    def build_tree(self, rectangle: RectangleArea, points: list[Point]) -> QuadtreeNode:
        node = QuadtreeNode(rectangle)

        # Dodaj punkty do węzła, jeśli nie przekraczają limitu
        if len(points) <= self.max_points_per_node:
            node.points = points
            self.vis.add_line_segment(((rectangle.min_x, rectangle.min_y), (rectangle.min_x, rectangle.max_y)))
            self.vis.add_line_segment(((rectangle.max_x, rectangle.min_y), (rectangle.max_x, rectangle.max_y)))
            self.vis.add_line_segment(((rectangle.min_x, rectangle.max_y), (rectangle.max_x, rectangle.max_y)))
            self.vis.add_line_segment(((rectangle.min_x, rectangle.min_y), (rectangle.max_x, rectangle.min_y)))
            return node

        # Inaczej, dzielimy przestrzeń na cztery ćwiartki
        mid_x = (rectangle.min_x + rectangle.max_x) / 2
        mid_y = (rectangle.min_y + rectangle.max_y) / 2

        # Tworzymy cztery podobszary
        quadrants = [
            RectangleArea(rectangle.min_x, rectangle.min_y, mid_x, mid_y),  # Lewy dolny
            RectangleArea(mid_x, rectangle.min_y, rectangle.max_x, mid_y),  # Prawy dolny
            RectangleArea(rectangle.min_x, mid_y, mid_x, rectangle.max_y),  # Lewy górny
            RectangleArea(mid_x, mid_y, rectangle.max_x, rectangle.max_y)   # Prawy górny
        ]

        

        # Dzielimy punkty na ćwiartki
        quadrant_points = [[] for _ in range(4)]
        for point in points:
            for i, q in enumerate(quadrants):
                if point in q:  # Punkt w obrębie danego kwadrantu
                    quadrant_points[i].append(point)
                    break

        # Tworzymy dzieci (ćwiartki) dla węzła
        node.is_leaf = False
        node.lower_left = self.build_tree(quadrants[0], quadrant_points[0])
        node.lower_right = self.build_tree(quadrants[1], quadrant_points[1])
        node.upper_left = self.build_tree(quadrants[2], quadrant_points[2])
        node.upper_right = self.build_tree(quadrants[3], quadrant_points[3])

        self.vis.add_line_segment(((rectangle.min_x, rectangle.min_y), (rectangle.min_x, rectangle.max_y)))
        self.vis.add_line_segment(((rectangle.max_x, rectangle.min_y), (rectangle.max_x, rectangle.max_y)))
        self.vis.add_line_segment(((rectangle.min_x, rectangle.max_y), (rectangle.max_x, rectangle.max_y)))
        self.vis.add_line_segment(((rectangle.min_x, rectangle.min_y), (rectangle.max_x, rectangle.min_y)))

        return node

    def find(self, rectangle: RectangleArea) -> list[Point]:
        return self.__find(self.root, rectangle)

    def __find(self, node: QuadtreeNode, rectangle: RectangleArea) -> list[Point]:
        res = []
        if node.rectangle & rectangle is None:  # Jeśli prostokąty nie mają wspólnego obszaru
            return res

        # Jeśli to liść, sprawdzamy punkty
        if node.is_leaf:
            res.extend([p for p in node.points if p in rectangle])
        else:
            # Rekurencyjnie sprawdzamy dzieci (cztery ćwiartki)
            if node.lower_left is not None:
                res.extend(self.__find(node.lower_left, rectangle))
            if node.lower_right is not None:
                res.extend(self.__find(node.lower_right, rectangle))
            if node.upper_left is not None:
                res.extend(self.__find(node.upper_left, rectangle))
            if node.upper_right is not None:
                res.extend(self.__find(node.upper_right, rectangle))

        return res

    def tree_print(self, node: QuadtreeNode):
        if node is not None:
            print(node)
            self.tree_print(node.upper_left)
            self.tree_print(node.upper_right)
            self.tree_print(node.lower_left)
            self.tree_print(node.lower_right)

    def get_vis(self):
        return self.vis
