import sys
import random
import math

class Centroid:
    def __init__(self, point, cluster_index):
        self.point_data = point
        self.cluster_index = cluster_index

class DataPoint:
    def __init__(self, data):
        self.data = data
        self.current_cluster = None
        self.previous_cluster = None


def calc_distance(center, point):
    center_data = center.point_data
    point_data = point.data

    sum_squared = 0
    for x, y in zip(point_data,center_data):
       sum_squared+= math.pow((x-y),2)
    euclidian_distance = math.sqrt(sum_squared)
    return euclidian_distance


def calc_center(points):
    sum_points = [0] * len(points[0])
    center = [0] * len(points[0])
    for point in points:
        for index, value in enumerate(point):
            sum_points[index] += value

    for index,value in enumerate(sum_points):
        center[index] = sum_points[index] / len(points)

    return center


def kmeans(data,k):
    data_tuples = open(data)

    processed_data = []
    for line in data_tuples:
        line = line.split(',')
        line.pop()
        processed_data += [line]


    integer_data = [[float(x) for x in line] for line in processed_data]

    center_points = []
    for index in range(0, k):
        center_point = Centroid(random.choice(integer_data), index)
        if center_point not in center_points:
            center_points.append(center_point)

    points = []
    for point in integer_data:
        points += [DataPoint(point)]

    while True:
        new_centers = False
        for point in points:

            min_distance = sys.float_info.max
            next_center = None
            for center in center_points:
                distance = calc_distance(center, point)

                if distance < min_distance:
                    min_distance = distance
                    next_center = center.cluster_index

            point.previous_cluster = point.current_cluster
            point.current_cluster = next_center

            if point.current_cluster != point.previous_cluster:
                new_centers = True
        if new_centers == False:
            break

        for center in center_points:
            center_cluster_data = [point.data for point in points if point.current_cluster == center.cluster_index]

            center_new_center = calc_center(center_cluster_data)
            center.point_data = center_new_center
    return center_points, points

def sse(center, points, k):
    center_by_index = [0] * len(center)

    for point in points:
        center_point = center[point.current_cluster]
        dist = calc_distance(center_point,point)
        center_by_index[point.current_cluster] += pow(dist,2)

    sum = 0
    for value in center_by_index:
        sum += value
    return sum


def output(points,output_file,sse_value):
    out = open(output_file, "w+")
    for point in points:
        predicted_cluster = point.current_cluster
        out.write(str(predicted_cluster))
        out.write("\n")
    out.write(str(sse_value))



if __name__ == '__main__':

    data = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]


    centers, points = kmeans(data,k)

    sse_value = sse(centers,points,k)

    output(points,output_file,sse_value)
    print("hello")