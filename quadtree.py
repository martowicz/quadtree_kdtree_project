import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from visualizer.main import Visualizer
from geo_structures import RectangleArea, Point


class Quadtree:
    def __init__(self, boundary, capacity):
        # Inicjalizacja Quadtree z prostokątem granicznym i maksymalną pojemnością punktów
        self.boundary = boundary  # Prostokąt definiujący granice tego Quadtree
        self.capacity = capacity  # Maksymalna liczba punktów przed podziałem
        self.points = []  # Lista punktów przechowywanych w tym Quadtree
        self.divided = False  # Czy Quadtree zostało podzielone na podregiony

    def subdivide(self):
        """Dzieli Quadtree na cztery mniejsze regiony."""
        x1, y1, x2, y2 = (
            self.boundary.min_x,
            self.boundary.min_y,
            self.boundary.max_x,
            self.boundary.max_y,
        )
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        # Tworzenie czterech podregionów: górny-lewy, górny-prawy, dolny-lewy, dolny-prawy
        self.upperleft = Quadtree(RectangleArea(x1, y, x, y2), self.capacity)
        self.upperright = Quadtree(RectangleArea(x, y, x2, y2), self.capacity)
        self.lowerleft = Quadtree(RectangleArea(x, y1, x2, y), self.capacity)
        self.lowerright = Quadtree(RectangleArea(x1, y1, x, y), self.capacity)

        self.divided = True  # Oznaczamy, że Quadtree zostało podzielone

    def insert(self, point):
        if not point in self.boundary:
            return False  # Punkt znajduje się poza granicami tego Quadtree

        if len(self.points) < self.capacity:
            # Jeśli mamy miejsce, dodajemy punkt
            self.points.append(point)
            return True

        if not self.divided:
            # Jeśli osiągnięto pojemność, dzielimy Quadtree na podregiony
            self.subdivide()

        # Próbujemy wstawić punkt do jednego z podregionów
        return (
            self.upperleft.insert(point)
            or self.upperright.insert(point)
            or self.lowerleft.insert(point)
            or self.lowerright.insert(point)
        )

    def find(self, range_rect, found_points=None):
        """Znajduje wszystkie punkty w danym prostokącie zapytania."""
        if found_points is None:
            found_points = []  # Inicjalizacja listy wynikowej

        if self.boundary & range_rect is None:
            return found_points  # Brak przecięcia, zwracamy pustą listę

        # Sprawdzamy punkty w bieżącym regionie
        for point in self.points:
            if point in range_rect:
                found_points.append(point)

        # Jeśli Quadtree jest podzielone, przeszukujemy podregiony
        if self.divided:
            self.upperleft.find(range_rect, found_points)
            self.upperright.find(range_rect, found_points)
            self.lowerleft.find(range_rect, found_points)
            self.lowerright.find(range_rect, found_points)

        return found_points

    def visualize(self, visualizer):
        """Wizualizuje Quadtree za pomocą klasy Visualizer."""
        # Dodaj granice tego Quadtree jako prostokąt
        x1 = self.boundary.min_x
        y1 = self.boundary.min_y
        x2 = self.boundary.max_x
        y2 = self.boundary.max_y

        visualizer.add_line_segment(((x1, y1), (x1, y2)))
        visualizer.add_line_segment(((x1, y1), (x2, y1)))
        visualizer.add_line_segment(((x2, y2), (x1, y2)))
        visualizer.add_line_segment(((x2, y2), (x2, y1)))

        # Dodaj punkty w tym Quadtree
        for point in self.points:
            visualizer.add_point((point.x, point.y), color="red")

        # Jeśli Quadtree jest podzielone, wizualizuj podregiony
        if self.divided:
            self.upperleft.visualize(visualizer)
            self.upperright.visualize(visualizer)
            self.lowerleft.visualize(visualizer)
            self.lowerright.visualize(visualizer)

        return visualizer
