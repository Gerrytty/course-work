from sklearn.cluster import DBSCAN
import math
import numpy as np


class Clusters:
    def __init__(self, d, labels):
        self.d = d
        self.labels = labels
        self.count_of_clusters = len(set(labels))


def get_clusters(points_array):

    clustering = DBSCAN(eps=3, min_samples=2).fit(points_array)

    count_of_clusters = len(set(clustering.labels_))

    d = dict()

    for i in range(count_of_clusters):
        d[i] = len(clustering.labels_[clustering.labels_ == i])

    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

    c = Clusters(d, clustering.labels_)

    return c


def get_cluster_points(points_array, clusters, position):

    cluster_points = []

    keys = list(clusters.d.keys())

    if position >= len(keys):
        return []

    for i, point in enumerate(points_array):
        point_cluster = clusters.labels[i]

        if point_cluster == keys[position]:
            cluster_points.append(point)

    return cluster_points


def get_nearest(clusters, point):

    distances = []

    for cluster in clusters:
        for cluster_point in cluster:
            distances.append(dist(point, cluster_point))

    distances.sort()

    return distances[0], distances[1]


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_distance(selected_point, canny):
    points_array = np.stack(np.nonzero(canny), axis=-1)

    clusters = get_clusters(points_array)

    cluster1 = get_cluster_points(points_array, clusters, 0)
    cluster2 = get_cluster_points(points_array, clusters, 1)

    nearest_point_in_first_cluster = min(cluster1, key=lambda p: dist(p, selected_point))
    nearest_point_in_second_cluster = min(cluster2, key=lambda p: dist(p, selected_point))

    distance = math.sqrt(
        (int(nearest_point_in_first_cluster[0]) - int(nearest_point_in_second_cluster[0])) ** 2 + (
                int(nearest_point_in_first_cluster[1]) - int(nearest_point_in_second_cluster[1])) ** 2)

    return nearest_point_in_first_cluster, nearest_point_in_second_cluster, distance