import time
from sys import setrecursionlimit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from quadtree import Quadtree
from kd_tree import KdTree
from geo_structures import RectangleArea, Point

setrecursionlimit(100000)


def print_table(df, filename):
    for n in sorted(list(set(df.n))):
        quad_time = df[(df.n == n) & (df.type == "quad")].time.mean()
        kd_time = df[(df.n == n) & (df.type == "kd")].time.mean()
        print(f"{n} & {quad_time:.4f} & {kd_time:.4f} \\\\")

    sns.lineplot(data=df, x="n", y="time", hue="type", errorbar="se")
    plt.ylabel("czas [s]")
    plt.legend(title="typ drzewa")
    plt.savefig(
        f"/home/wiktoro/Studia/Geometryczne/quadtree_kdtree_project/graphs/{filename}.pdf"
    )
    plt.clf()


def calculate(distribution, ns, filename_prefix):
    construction_times = []
    small_find_times = []
    big_find_times = []

    for n in ns:
        print(n)
        for _ in range(15):
            points = distribution(n)
            small_rectangle = get_small_rectangle()  # 1/100
            big_rectangle = get_big_rectangle()  # 1/4

            start_time = time.process_time()
            tree1 = Quadtree(points)
            construction_times.append([n, "quad", time.process_time() - start_time])
            start_time = time.process_time()
            tree2 = KdTree(points)
            construction_times.append([n, "kd", time.process_time() - start_time])

            start_time = time.process_time()
            f1 = tree1.find(small_rectangle)
            small_find_times.append([n, "quad", time.process_time() - start_time])
            start_time = time.process_time()
            f2 = tree2.find(small_rectangle)
            small_find_times.append([n, "kd", time.process_time() - start_time])
            assert set(f1) == set(f2)

            start_time = time.process_time()
            f1 = tree1.find(big_rectangle)
            big_find_times.append([n, "quad", time.process_time() - start_time])
            start_time = time.process_time()
            f2 = tree2.find(big_rectangle)
            big_find_times.append([n, "kd", time.process_time() - start_time])
            assert set(f1) == set(f2)

    construction_times = pd.DataFrame(construction_times, columns=["n", "type", "time"])
    small_find_times = pd.DataFrame(small_find_times, columns=["n", "type", "time"])
    big_find_times = pd.DataFrame(big_find_times, columns=["n", "type", "time"])

    print_table(construction_times, filename_prefix + "_construction_time")
    print_table(small_find_times, filename_prefix + "_find_small_time")
    print_table(big_find_times, filename_prefix + "_find_big_time")














def get_small_rectangle():
    x = np.random.uniform(-1000, 980)
    y = np.random.uniform(-1000, 980)
    return RectangleArea(x, y, x + 20, y + 20)


def get_big_rectangle():
    x = np.random.uniform(-1000, 0)
    y = np.random.uniform(-1000, 0)
    return RectangleArea(x, y, x + 1000, y + 1000)






def uniformly_distributed_points(n):
    return [
        Point(x, y)
        for x, y in zip(
            np.random.uniform(-1000, 1000, n), np.random.uniform(-1000, 1000, n)
        )
    ]


def pair_of_points(n):
    points = []
    points.append(Point(1000, 1000))

    for _ in range(n // 2):
        x = np.random.uniform(-100, 100)
        y = np.random.uniform(-100, 100)
        points.append(Point(x, y))
        points.append(Point(x + 1e-8, y))
    return points


# Testowanie funkcji z różnymi rozkładami punktów

#calculate(uniformly_distributed_points, (10_000, 20_000, 30_000, 40_000), 'uniform')
calculate(pair_of_points, (10_000, 15_000), "pairs")
