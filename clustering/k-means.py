# k-means

import matplotlib.pyplot as plt
import generate as generate


class Point:
    def __init__(self, c):
        if c is None:
            self.length = 0
            self.coordinates = []
        else:
            self.length = len(c)
            self.coordinates = []
            for i in range(self.length):
                self.coordinates.append(c[i])

    def get_data(self):
        return self.coordinates

    def print(self):
        print("{0} ".format(list(self.coordinates)), end="")


class Cluster:
    def __init__(self):
        self.clusterMembers = []

    def get_data(self):
        t = []
        for point in self.clusterMembers:
            t.append(point.coordinates)
        return t

    def union(self, other):
        if not (other is None) and not (other.clusterMembers is None):
            for p in other.clusterMembers:
                self.clusterMembers.append(p)

    def insert(self, p):
        self.clusterMembers.append(p)

    def get_center(self):
        if len(self.clusterMembers) == 0:
            return None
        avg = [0] * len(self.clusterMembers[0].coordinates)
        for point in self.clusterMembers:
            for i in range(len(point.coordinates)):
                avg[i] += point.coordinates[i]
        l = len(self.clusterMembers)
        for i in range(len(avg)):
            avg[i] = avg[i] / l
        return Point(avg)

    def print(self):
        print("Length = {0}\n".format(len(self.clusterMembers)), end="")
        for point in self.clusterMembers:
            point.print()
        print("\n\n", end="")


def distance(a, b):
    from math import sqrt
    s = 0
    for i in range(a.length):
        s += (a.coordinates[i] - b.coordinates[i]) ** 2
    return sqrt(s)


def print_clusters(clusters):
    print("Clusters List : Length = {0}\n\n".format(len(clusters)), end="")
    for cluster in clusters:
        cluster.print()
    print("\n\n")


def plot_2d(clusters, plot_center):
    # plot each cluster in different color, if plot_center is True
    # also the center of each cluster will be draw
    if ((clusters is not None) and
            (clusters[0] is not None) and
            (clusters[0].clusterMembers[0] is not None)):
        if len(clusters[0].clusterMembers[0].coordinates) == 2:
            for cluster in clusters:
                # print(cluster)
                colx = [p.coordinates[0] for p in cluster.clusterMembers]
                coly = [p.coordinates[1] for p in cluster.clusterMembers]
                plt.scatter(colx, coly)
                if plot_center:
                    center = cluster.get_center()
                    plt.scatter([center.coordinates[0]], [
                                center.coordinates[1]], s=80, c='b')

            plt.show()
            plt.gcf().clear()


def get_clusters(points, num_of_clusters):
    # create cluster for each point
    clusters = []
    for i in range(len(points)):
        t = Cluster()
        t.insert(points[i])
        clusters.append(t)

    l = len(clusters)

    # build distance matrix based on the center
    result_matrix = []
    for i in range(l):
        result_matrix.append([])
        for j in range(l):
            result_matrix[i].append(0.0)

    for i in range(l):
        for j in range(i):
            result_matrix[i][j] = distance(
                clusters[i].get_center(), clusters[j].get_center())
            result_matrix[j][i] = result_matrix[i][j]

    while l > num_of_clusters:
        if l == 1:
            return clusters  # one cluster

        # find the minimum distance between two different clusters
        min_i = 0
        min_j = 1

        for i in range(l):
            for j in range(l):
                if (result_matrix[i][j] < result_matrix[min_i][min_j] and
                        i != j):
                    min_i = i
                    min_j = j

        # union between the clusters
        clusters[min_i].union(clusters[min_j])
        center = clusters[min_i].get_center()

        # update result matrix for the distances for the new cluster
        for i in range(l):
            result_matrix[i][min_i] = distance(
                clusters[i].get_center(), center)

        clusters.pop(min_j)

        # update result matrix
        for i in range(l):
            result_matrix[i].pop(min_j)
        result_matrix.pop(min_j)

        l -= 1

    return clusters


def run(matrix, num_of_clusters):
    points = []
    for row in matrix:
        points.append(Point(row))
    return get_clusters(points, num_of_clusters)


def main():
    number_of_points = 100
    random_matrix = generate.gen(2, number_of_points)

    clusters_count = 5

    while clusters_count <= int(number_of_points / 10):
        c = run(random_matrix, clusters_count)
        print_clusters(c)
        plot_2d(c, True)
        clusters_count += 5


if __name__ == '__main__':
    main()
