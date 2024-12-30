import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from visualizer.main import Visualizer
from geo_structures import RectangleArea, Point

class Point:
    def __init__(self, x, y):
        # Punkt w dwuwymiarowej przestrzeni
        self.x = x
        self.y = y

    def __repr__(self):
        # Reprezentacja punktu jako tekst
        return f"Point({self.x}, {self.y})"


class Boundary:
    def __init__(self, x, y, width, height):
        # Prostokąt definiowany przez lewy górny róg (x, y), szerokość i wysokość
        self.x = x  # Współrzędna x lewego górnego rogu
        self.y = y  # Współrzędna y lewego górnego rogu
        self.width = width  # Szerokość prostokąta
        self.height = height  # Wysokość prostokąta

    def contains(self, point):
        """Sprawdza, czy punkt znajduje się w obrębie prostokąta."""
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def intersects(self, range_rect):
        """Sprawdza, czy prostokąt przecina się z innym prostokątem."""
        return not (range_rect.x > self.x + self.width or
                    range_rect.x + range_rect.width < self.x or
                    range_rect.y > self.y + self.height or
                    range_rect.y + range_rect.height < self.y)


class Quadtree:
    def __init__(self, boundary, capacity):
        # Inicjalizacja Quadtree z prostokątem granicznym i maksymalną pojemnością punktów
        self.boundary = boundary  # Prostokąt definiujący granice tego Quadtree
        self.capacity = capacity  # Maksymalna liczba punktów przed podziałem
        self.points = []  # Lista punktów przechowywanych w tym Quadtree
        self.divided = False  # Czy Quadtree zostało podzielone na podregiony

    def subdivide(self):
        """Dzieli Quadtree na cztery mniejsze regiony."""
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height
        half_w, half_h = w / 2, h / 2

        # Tworzenie czterech podregionów: górny-lewy, górny-prawy, dolny-lewy, dolny-prawy
        self.upperleft = Quadtree(Boundary(x, y, half_w, half_h), self.capacity)
        self.upperright = Quadtree(Boundary(x + half_w, y, half_w, half_h), self.capacity)
        self.lowerleft = Quadtree(Boundary(x, y + half_h, half_w, half_h), self.capacity)
        self.lowerright = Quadtree(Boundary(x + half_w, y + half_h, half_w, half_h), self.capacity)

        self.divided = True  # Oznaczamy, że Quadtree zostało podzielone

    def insert(self, point):
        if not self.boundary.contains(point):
            return False  # Punkt znajduje się poza granicami tego Quadtree

        if len(self.points) < self.capacity:
            # Jeśli mamy miejsce, dodajemy punkt
            self.points.append(point)
            return True

        if not self.divided:
            # Jeśli osiągnięto pojemność, dzielimy Quadtree na podregiony
            self.subdivide()


        # Próbujemy wstawić punkt do jednego z podregionów
        return (self.upperleft.insert(point) or
                self.upperright.insert(point) or
                self.lowerleft.insert(point) or
                self.lowerright.insert(point))

    def query(self, range_rect, found_points=None):
        """Znajduje wszystkie punkty w danym prostokącie zapytania."""
        if found_points is None:
            found_points = []  # Inicjalizacja listy wynikowej

        if not self.boundary.intersects(range_rect):
            return found_points  # Brak przecięcia, zwracamy pustą listę

        # Sprawdzamy punkty w bieżącym regionie
        for point in self.points:
            if range_rect.contains(point):
                found_points.append(point)

        # Jeśli Quadtree jest podzielone, przeszukujemy podregiony
        if self.divided:
            self.upperleft.query(range_rect, found_points)
            self.upperright.query(range_rect, found_points)
            self.lowerleft.query(range_rect, found_points)
            self.lowerright.query(range_rect, found_points)

        return found_points

    def visualize(self, visualizer):
        """Wizualizuje Quadtree za pomocą klasy Visualizer."""
        # Dodaj granice tego Quadtree jako prostokąt
        x=self.boundary.x
        y=self.boundary.y
        width = self.boundary.width
        height = self.boundary.height
        visualizer.add_line_segment(((x,y),(x,y+height)))
        visualizer.add_line_segment(((x,y),(x+width,y)))
        visualizer.add_line_segment(((x+width,y),(x+width,y+height)))
        visualizer.add_line_segment(((x,y+height),(x+width,y+height)))


        # Dodaj punkty w tym Quadtree
        for point in self.points:
            visualizer.add_point((point.x, point.y), color='red')

        # Jeśli Quadtree jest podzielone, wizualizuj podregiony
        if self.divided:
            self.upperleft.visualize(visualizer)
            self.upperright.visualize(visualizer)
            self.lowerleft.visualize(visualizer)
            self.lowerright.visualize(visualizer)

        return visualizer

    def __repr__(self):
        # Reprezentacja Quadtree jako tekst
        return self.vis.show()
