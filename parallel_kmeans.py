import math
import random
import multiprocessing
import time


def calculate_centroid_distances(args):
    # centroid_index, x_coords, y_coords, x_centroid, y_centroid = args
    # distances = []
    # for i in range(len(x_coords)):
    #     dist = math.sqrt((x_coords[i] - x_centroid)**2 + (y_coords[i] - y_centroid)**2)
    #     distances.append(dist)
    # return distances
    x, y, x_centroids, y_centroids = args
    return [math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in zip(x_centroids, y_centroids)]


def calculateDistance(x_coords, y_coords, x_centroids, y_centroids):
    with multiprocessing.Pool() as pool:
        tasks = [(x_coords[i], y_coords[i], x_centroids, y_centroids) for i in range(len(x_coords))]
        distances = pool.map(calculate_centroid_distances, tasks)

    # distances = list(map(list, zip(*results)))
    return distances


def assignNodes(distances):
    assignments = []

    for point_distances in distances:
        closest_centroid = point_distances.index(min(point_distances))
        assignments.append(closest_centroid)

    return assignments


def recalculateCentroids(assignments, x_coords, y_coords, centNum):
    new_x_centroids = [0.0] * centNum
    new_y_centroids = [0.0] * centNum
    counts = [0] * centNum

    for i in range(len(assignments)):
        cluster = assignments[i]
        new_x_centroids[cluster] += x_coords[i]
        new_y_centroids[cluster] += y_coords[i]
        counts[cluster] += 1

    for i in range(centNum):
        if counts[i] != 0:
            new_x_centroids[i] /= counts[i]
            new_y_centroids[i] /= counts[i]

    return new_x_centroids, new_y_centroids


def fileToList():
    with open("clustering.txt", "r") as file:
        lines = file.readlines()

    x_coords = list(map(float, lines[0].split()))
    y_coords = list(map(float, lines[1].split()))

    return x_coords, y_coords


def findCentroids(x_coords, y_coords):
    listLen = len(x_coords)
    if listLen <= 10:
        centNum = 2
    elif 10 < listLen <= 20:
        centNum = 3
    else:
        centNum = 4

    selected_indices = random.sample(range(listLen), centNum)

    x_centroids = [x_coords[i] for i in selected_indices]
    y_centroids = [y_coords[i] for i in selected_indices]

    with open("data.txt", "w") as file:
        file.write(" ".join(str(x) for x in x_centroids) + "\n")
        file.write(" ".join(str(y) for y in y_centroids) + "\n")

    return x_centroids, y_centroids, centNum


if __name__ == "__main__":
    start = time.time()
    x_coords, y_coords = fileToList()
    x_centroids, y_centroids, centNum = findCentroids(x_coords, y_coords)
    print(x_centroids)
    print(y_centroids)

    for i in range(10):
        distances = calculateDistance(x_coords, y_coords, x_centroids, y_centroids)
        assignments = assignNodes(x_coords, y_coords, x_centroids, y_centroids, distances)
        x_centroids, y_centroids = recalculateCentroids(assignments, x_coords, y_coords, centNum)

    end = time.time()

    print("The coordinates used were:")
    print(f"{x_coords}\n{y_coords}\n")
    print("The final centroids are:")
    print(f"{x_centroids}\n{y_centroids}\n")
    print("The final assignments were:")
    print(assignments)
    print(f"This took {end-start} time.")