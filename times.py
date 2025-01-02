import time
from sys import setrecursionlimit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geo_structures import RectangleArea, Point
from quadtree import Quadtree
from kd_tree import KdTree

setrecursionlimit(100000)
plt.style.use("_classic_test_patch")
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.linewidth"] = 0.5


def get_time(generate_points, n_list, data_type_name):

    tree_construct_time = []
    small_rect_time = []
    big_rect_time = []

    for n in n_list:
        print(n)
        for _ in range(10):


            small_rectangle = RectangleArea(2500, 2500, 2500 + 25, 2500 + 25)
            big_rectangle = RectangleArea(2500, 2500, 2500 +  1000, 2500 + 1000)
            points = generate_points(n)

            start_time = time.process_time()
            tree_quad = Quadtree(points)
            stop_time = time.process_time()
            tree_construct_time.append([n, "quad", stop_time - start_time])

            start_time = time.process_time()
            tree_kd = KdTree(points)
            stop_time = time.process_time()
            tree_construct_time.append([n, "kd", stop_time - start_time])

            start_time = time.process_time()
            f1 = tree_quad.find(small_rectangle)
            stop_time = time.process_time()
            small_rect_time.append([n, "quad", stop_time - start_time])

            start_time = time.process_time()
            f2 = tree_kd.find(small_rectangle)
            stop_time = time.process_time()
            small_rect_time.append([n, "kd", stop_time - start_time])

            assert set(f1) == set(f2)
            # dodatkowo sprawdzam czy obydwa algorytmy dały ten sam wynik

            start_time = time.process_time()
            f1 = tree_quad.find(big_rectangle)
            stop_time = time.process_time()
            big_rect_time.append([n, "quad", stop_time - start_time])

            start_time = time.process_time()
            f2 = tree_kd.find(big_rectangle)
            stop_time = time.process_time()
            big_rect_time.append([n, "kd", stop_time - start_time])

            assert set(f1) == set(f2)
            # dodatkowo sprawdzam czy obydwa algorytmy dały ten sam wynik

    tree_construct_time = pd.DataFrame(
        tree_construct_time, columns=["n", "type", "time"]
    )
    small_rect_time = pd.DataFrame(small_rect_time, columns=["n", "type", "time"])
    big_rect_time = pd.DataFrame(big_rect_time, columns=["n", "type", "time"])

    generate_graph(tree_construct_time, data_type_name + "_tree_construction_time")
    generate_graph(small_rect_time, data_type_name + "_small_rect_time")
    generate_graph(big_rect_time, data_type_name + "_big_rect_time")


def generate_graph(df, filename):

    # wypisuje dane do tabeli w formacie typst

    for n in sorted(
        list(set(df.n))
    ):  # Iteruje po unikalnych wartościach n (liczbie punktów) w DataFrame.
        quad_time = df[
            (df.n == n) & (df.type == "quad")
        ].time.mean()  # liczy średnią dla danego n i danego typu algorytmu
        kd_time = df[(df.n == n) & (df.type == "kd")].time.mean()
        print(f"[${n}$],[${quad_time:.4f}$],[${kd_time:.4f}$],")

    sns.lineplot(
        data=df, x="n", y="time", hue="type", errorbar="se"
    )  # dodaje osie oraz wykres wraz ze standardowym błędem średniej

    plt.ylabel("czas [s]")  # etykieta osi pionowej
    plt.legend(title="typ drzewa")  # legenda
    plt.savefig(
        f"/home/wiktoro/Studia/Geometryczne/quadtree_kdtree_project/graphs/{filename}.pdf"
    )  # ścieżka do folderu z wykresami
    plt.clf()  # czyści obecne dane w plt


def uniform_points(n):
    return [
        Point(x, y)
        for x, y in zip(np.random.uniform(0, 5000, n), np.random.uniform(0, 5000, n))
    ]


def normal_points(n):
    points = []
    for x, y in np.random.normal(2500, 650, (n, 2)):
        points.append(Point(x, y))

    return points


def clusters_points(n):
    points = []

    for _ in range(n // 5):
        points.append(
            Point(np.random.uniform(1000, 1400), np.random.uniform(1000, 1600))
        )
        points.append(
            Point(np.random.uniform(3000, 3500), np.random.uniform(3000, 3500))
        )
        points.append(Point(np.random.uniform(4000, 4500), np.random.uniform(0, 500)))
        points.append(
            Point(np.random.uniform(500, 1000), np.random.uniform(4000, 4500))
        )
        points.append(
            Point(np.random.uniform(2500, 3000), np.random.uniform(2000, 2500))
        )

    return points


# Testowanie funkcji z różnymi rozkładami punktów
ns = [2000,10000, 20000,30000,40000,50000]

get_time(uniform_points, ns, "uniform")
get_time(normal_points, ns, "normal")
get_time(clusters_points, ns, "clusters")
